from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from .forms import CustomerRegistrationForm
from .models import Fruit
from django.contrib import messages
from django.shortcuts import render, redirect



# Fruit list

class FruitListView(View):
    def get(self, request):
        fruits = Fruit.objects.all()
        return render(request, 'index.html', {'fruits': fruits})


# Fruit details

class FruitDetail(View):
    def get(self, request, id):
        fruit = Fruit.objects.get(id=id)
        return render(request, 'product-single.html', {'fruit': fruit})


#account creation

class CustomRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
        return render(request, 'signup.html', {'form': form})
