from django.contrib import admin
from . import models
import stripe


class OrderPositionInline(admin.TabularInline):
    model = models.OrderPosition


class DiscountAdmin(admin.ModelAdmin):
    fields = ['name', 'percentage']

    def save_model(self, request, obj, form, change):

        coupon = stripe.Coupon.create(percent_off=obj.percentage, duration="once")

        obj.stripe_coupon_id = coupon.id
        return super(DiscountAdmin, self).save_model(request, obj, form, change)


class TaxAdmin(admin.ModelAdmin):
    fields = ['name', 'percentage']

    def save_model(self, request, obj, form, change):

        tax_rate = stripe.TaxRate.create(
            display_name=obj.name,
            inclusive=obj.inclusive,
            percentage=obj.percentage,
        )
        obj.stripe_tax_id = tax_rate.id
        return super(TaxAdmin, self).save_model(request, obj, form, change)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderPositionInline, )


admin.site.register(models.Discount, DiscountAdmin)
admin.site.register(models.Tax, TaxAdmin)
admin.site.register(models.Item)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderPosition)
