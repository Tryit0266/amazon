from django.contrib import admin
from .models import Item, Category, Color, Rate, OrderItem, Order, Address1, CreditCardPayment, Otp, UploadImage


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id',]
    prepopulated_fields = {"slug": ("name",)}

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'id',]
    prepopulated_fields = {"slug": ("name",)}

class RateAdmin(admin.ModelAdmin):
    list_display = ['name', 'id',]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Rate, RateAdmin)
admin.site.register(Address1)
admin.site.register(CreditCardPayment)
admin.site.register(Otp)
admin.site.register(UploadImage)

