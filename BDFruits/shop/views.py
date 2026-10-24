from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import CustomerRegistrationForm, LoginForm, CustomerProfileForm, CustomerAddressForm
from .models import Fruit, Customer, CustomerAddress, Cart
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
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
        addresses = CustomerAddress.objects.filter(user=request.user)
        show_form = request.GET.get('new') == '1'
        form = CustomerAddressForm() if show_form else None
        return render(request, 'address.html', {
            'addresses': addresses,
            'address': form,
            'show_form': show_form,
        })

    def post(self, request):
        addresses = CustomerAddress.objects.filter(user=request.user)
        form = CustomerAddressForm(request.POST)
        if form.is_valid():
            customer_address = form.save(commit=False)
            customer_address.user = request.user
            customer_address.save()
            messages.success(request, 'Congratulations! Address added successfully!')
            return redirect('address')
        return render(request, 'address.html', {
            'addresses': addresses,
            'address': form,
            'show_form': True,
        })


#add to cart
@login_required(login_url='/login/')
def add_to_cart(request, fruit_id):
    fruit = get_object_or_404(Fruit, id=fruit_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, fruit=fruit)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, 'Item added to cart.')
    return redirect('showcart')



def show_cart(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    carts = Cart.objects.filter(user=request.user)
    amount = 0.0
    shipping_amount = 100.0
    for item in carts:
        amount += item.line_total
    total_amount = amount + shipping_amount if carts else 0.0
    return render(request, 'cart.html', {
        'carts': carts,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'totalamount': total_amount,
    })