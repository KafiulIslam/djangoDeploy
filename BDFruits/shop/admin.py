from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Fruit, Customer, CustomerAddress, OrderPlaced

@admin.register(Fruit)
class FruitAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'fruit_image']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'division', 'district', 'thana', 'villorroad', 'zipcode']


@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'division', 'district', 'thana', 'roadNumber', 'zipCode', 'addressType']

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'fruit', 'quantity', 'payment_method', 'status', 'tran_id', 'ordered_date']


