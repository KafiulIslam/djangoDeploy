from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from .models import Fruit


# Create your views here.

class FruitListView(View):
    def get(self, request):
        fruits = Fruit.objects.all()
        return render(request, 'index.html', {'fruits': fruits})
