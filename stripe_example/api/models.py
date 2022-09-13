from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib import admin
import stripe

# Create your models here.


class DiscountAdmin(admin.ModelAdmin):
    fields = ['name', 'percentage']

    def save_model(self, request, obj, form, change):

        coupon = stripe.Coupon.create(percent_off=obj.percentage, duration="once")

        obj.stripe_coupon_id = coupon.id
        return super(DiscountAdmin, self).save_model(request, obj, form, change)


class Discount(models.Model):
    name = models.CharField(max_length=50)
    percentage = models.PositiveIntegerField(default=None, validators=[MaxValueValidator(99), MinValueValidator(0)], help_text='0 to 99%')
    stripe_coupon_id = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name} {self.percentage}%'


class TaxAdmin(admin.ModelAdmin):
    fields = ['name', 'percentage']

    def save_model(self, request, obj, form, change):

        tax_rate = stripe.TaxRate.create(
            display_name=obj.name,
            inclusive=False,
            percentage=obj.percentage,
        )
        obj.stripe_tax_id = tax_rate.id
        return super(TaxAdmin, self).save_model(request, obj, form, change)


class Tax(models.Model):
    name = models.CharField(max_length=20)
    percentage = models.PositiveIntegerField(default=None, validators=[MaxValueValidator(99), MinValueValidator(0)], help_text='0 to 99%')
    stripe_tax_id = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name} {self.percentage}%'


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name


class Order(models.Model):
    order_position = models.ManyToManyField("self", through='OrderPosition')
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, default=None, null=True, blank=True)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE, default=None, null=True, blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Заказ: {self.id}"


class OrderPosition(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Заказ: {self.order.id} Предмет: {self.item.name} {self.quantity} шт."

    class Meta:
        unique_together = ('order', 'item')