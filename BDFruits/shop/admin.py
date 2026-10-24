from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Fruit, Customer

@admin.register(Fruit)
class FruitAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'fruit_image']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'division', 'district', 'thana', 'villorroad', 'zipcode']