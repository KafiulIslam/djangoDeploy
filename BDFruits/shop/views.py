from django.views import View
from .forms import CustomerRegistrationForm, LoginForm, CustomerProfileForm, CustomerAddressForm
from .models import Fruit, Customer, CustomerAddress
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


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


# account creation
class CustomRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful.')
            return redirect('/')
        return render(request, 'signup.html', {'form': form})


# Login
class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('/')

    def form_valid(self, form):
        messages.success(self.request, 'Logged in successfully.')
        return super().form_valid(form)


# Customer profile
class CustomerProfileView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        customer = Customer.objects.filter(user=request.user).first()
        form = CustomerProfileForm(instance=customer)
        return render(request, 'profile.html', {'form': form})

    def post(self, request):
        customer = Customer.objects.filter(user=request.user).first()
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Congratulations! Profile updated successfully!')
            return redirect('profile')
        return render(request, 'profile.html', {'form': form})


# Customer Address
class CustomerAddressView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request):
        address = CustomerAddress.objects.filter(user=request.user).first()
        form = CustomerAddressForm(instance=address)
        return render(request, 'address.html', {'address': form})

    def post(self, request):
        address = CustomerAddress.objects.filter(user=request.user).first()
        form = CustomerAddressForm(request.POST, instance=address)
        if form.is_valid():
            customerAddress = form.save(commit=False)
            customerAddress.user = request.user
            customerAddress.save()
            messages.success(request, 'Congratulations! Address updated successfully!')
            return redirect('address')
        return render(request, 'address.html', {'address': form})