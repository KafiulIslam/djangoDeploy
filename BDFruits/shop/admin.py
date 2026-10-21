from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Fruit

@admin.register(Fruit)
class FruitAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'fruit_image']