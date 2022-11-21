from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Discount(models.Model):
    name = models.CharField(max_length=50)
    percentage = models.PositiveIntegerField(
        default=None,
        validators=[MaxValueValidator(99), MinValueValidator(0)],
        help_text='0 to 99%')
    stripe_coupon_id = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name} {self.percentage}%'

    class Meta:
        db_table = "content\".\"discount"


class Tax(models.Model):
    name = models.CharField(max_length=20)
    percentage = models.PositiveIntegerField(
        default=20,
        validators=[MaxValueValidator(99), MinValueValidator(0)],
        help_text='0 to 99%'
    )
    stripe_tax_id = models.CharField(max_length=200)
    inclusive = models.BooleanField(
        default=True,
        help_text='True for inclusion tax in price'
    )

    def __str__(self):
        return f'{self.name} {self.percentage}%'

    class Meta:
        db_table = "content\".\"tax"


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, default=None, null=True, blank=True)
    price = models.DecimalField(max_digits=2, decimal_places=0, validators=[MinValueValidator(1)])
    src_url = models.URLField(default=None, null=True, blank=True, help_text='link to image file')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"item"


class OrderPosition(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Заказ: {self.order.id} Предмет: {self.item.name} {self.quantity} шт."

    class Meta:
        db_table = "content\".\"order_position"
        unique_together = ('order', 'item')


class Order(models.Model):
    order_position = models.ManyToManyField('self', through='OrderPosition')
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, default=None, null=True, blank=True)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE, default=None, null=True, blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Заказ: {self.id}"

    class Meta:
        db_table = "content\".\"order"
