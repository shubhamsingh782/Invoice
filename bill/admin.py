from django.contrib import admin
from .models import Order, Product, Purchase
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
	list_display = ('user','contact','address','total_product_cost','tax','order_made_on')

class ProductAdmin(admin.ModelAdmin):
	list_display = ('product_name','cost')

class PurchaseAdmin(admin.ModelAdmin):
	list_display = ('order', 'product','quantity')

admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Purchase, PurchaseAdmin)