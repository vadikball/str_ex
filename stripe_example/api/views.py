from django.shortcuts import render, get_object_or_404
from django.views import View
from . import models
from django.http import JsonResponse
import stripe
import os
from typing import Union, List


def _get_amount(positions: List[models.OrderPosition], order: models.Order) -> int:
    """ Подсчитывает итог заказа """

    amount = 0
    for position in positions:
        amount += position.quantity * int(position.item.price*100)
    if order.discount:
        amount = amount - (round(amount * (order.discount.percentage / 100), 2))
    return amount


def _line_items_prep(input_object: Union[models.Item, models.Order]) -> list:
    """ Подготавливает список line_items для создания stripe.checkout.Session """
    if isinstance(input_object, models.Item):
        var_tuple = ((input_object.name, int(input_object.price * 100), 1,), )
    else:
        var_tuple = tuple(
            (
                pos.item.name,
                int(pos.item.price*100),
                pos.quantity,
            ) for pos in input_object.order_position
        )

    additional_info = {}
    if isinstance(input_object, models.Order) and input_object.tax is not None:
        additional_info = {'tax_rates': [input_object.tax.stripe_tax_id]}

    line_items = [additional_info.update({
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': pos[0],
            },
            'unit_amount': pos[1],
        },
        'quantity': pos[2],
    }) for pos in var_tuple]

    return line_items


class MainPage(View):
    template_name = 'api/main.html'

    def get(self, request):
        return render(request, self.template_name)


class GetItem(View):
    model = models.Item
    template_name = 'api/get_item.html'

    def get(self, request, pk):
        """ HTML страница с информацией о товаре """

        item = get_object_or_404(self.model, id=pk)

        ctx = {'item': item}
        return render(request, self.template_name, context=ctx)


class BuyItem(View):
    model = models.Item

    def get(self, request, pk):

        """ :return JSON объект с созданной stripe.checkout.Session """
        item = get_object_or_404(self.model, id=pk)

        session = stripe.checkout.Session.create(
            line_items=_line_items_prep(item),
            mode='payment',
            success_url=f'{os.environ.get("APP_URL", "http://localhost:8000")}/success',
            cancel_url=f'{os.environ.get("APP_URL", "http://localhost:8000")}',
        )
        return JsonResponse(session)


class SuccessPage(View):
    template_name = 'api/success.html'

    def get(self, request):
        """ HTML страница с информацией об успехе """

        return render(request, self.template_name)


class SuccessPageOrder(View):
    template_name = 'api/success.html'
    model = models.Order

    def get(self, request, pk):
        """ HTML страница с информацией об успехе для заказа """

        order = get_object_or_404(self.model, id=pk)
        if not order.paid:
            order.paid = True
            order.save()
        return render(request, self.template_name)


class GetOrder(View):
    template_name = 'api/get_order.html'
    model = models.Order

    def get(self, request, pk):
        """ HTML страница с информацией о заказе, если заказ оплачен - рендерит 'api/success.html' """

        return_url = f'{os.environ.get("APP_URL", "http://localhost:8000")}/intent/{pk}/status'
        order = get_object_or_404(self.model, id=pk)
        if order.paid:
            return render(request, SuccessPage.template_name)
        else:
            positions = list(models.OrderPosition.objects.filter(order=order))
            total = round(_get_amount(positions, order) / 100, 2)
            ctx = {'order': order, 'positions': positions, 'total': total, 'return_url': return_url}
            return render(request, self.template_name, context=ctx)


class BuyOrder(View):
    model = models.Order

    def get(self, request, pk):
        """ :return JSON объект с созданной stripe.checkout.Session """

        order = get_object_or_404(self.model, id=pk)
        if order.paid:
            return render(request, SuccessPage.template_name)
        else:
            positions = list(self.model.objects.select_related().prefetch_related().filter(order=order))

            session = stripe.checkout.Session.create(
                line_items=_line_items_prep(positions),
                mode='payment',
                success_url=f'{os.environ.get("APP_URL", "http://localhost:8000")}/success',
                cancel_url=f'{os.environ.get("APP_URL", "http://localhost:8000")}',
                discounts=[{
                    'coupon': order.discount.stripe_coupon_id
                }],

            )
            return JsonResponse(session)


class CreatePaymentIntent(View):
    model = models.Order

    def get(self, request, pk):
        """ Создаёт stripe.PaymentIntent
            :return JSON объект с 'clientSecret' """

        order = get_object_or_404(self.model, id=pk)
        if order.paid:
            return render(request, SuccessPage.template_name)
        else:
            positions = list(models.OrderPosition.objects.filter(order=order))
            amount = int(_get_amount(positions, order))
            payment_intent = stripe.PaymentIntent.create(
                currency='usd',
                amount=amount,
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            return JsonResponse({'clientSecret': payment_intent['client_secret']})


class IntentStatus(View):
    template_name = 'api/status.html'

    def get(self, request, pk):
        """ HTML страница с информацией об успехе для заказа при оплате через stripe.PaymentIntent """

        ctx = {'pk': pk}
        return render(request, self.template_name, context=ctx)


class IntentStatusSuccess(View):
    model = models.Order

    def get(self, request, pk):
        """ endpoint чтобы присвоить заказу статус "Оплачен" при оплате через stripe.PaymentIntent """

        order = get_object_or_404(self.model, id=pk)
        order.paid = True
        order.save()
        return JsonResponse({'status': 'success'})


class PubKey(View):

    def get(self, request):
        pub_key = os.environ.get('PUB_KEY')
        return JsonResponse({'pub_key': pub_key})

