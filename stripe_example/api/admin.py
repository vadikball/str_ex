from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Discount, models.DiscountAdmin)
admin.site.register(models.Tax, models.TaxAdmin)
admin.site.register(models.Item)
admin.site.register(models.Order)
admin.site.register(models.OrderPosition)
