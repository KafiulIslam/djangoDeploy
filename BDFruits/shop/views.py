from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import CustomerRegistrationForm, LoginForm, CustomerProfileForm, CustomerAddressForm
from .models import Fruit, Customer, CustomerAddress, Cart, OrderPlaced
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from sslcommerz_lib import SSLCOMMERZ
from decimal import Decimal
from django.contrib.auth.models import User

from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
import uuid


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


# add to cart
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


@login_required(login_url='/login/')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    addresses = CustomerAddress.objects.filter(user=request.user)
    amount = 0.0
    shipping_amount = 100.0
    for item in cart_items:
        amount += item.line_total
    total_amount = amount + shipping_amount if cart_items else 0.0

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'addresses': addresses,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'totalamount': total_amount,
    })


def _customer_for_order(user, address):
    """OrderPlaced needs a Customer row. Use the profile, or copy the chosen address."""
    customer = Customer.objects.filter(user=user).first()
    if customer:
        return customer
    return Customer.objects.create(
        user=user,
        name=user.get_full_name() or user.username,
        division=address.division,
        district=address.district,
        thana=address.thana,
        villorroad=address.roadNumber[:100],
        zipcode=address.zipCode,
    )


def _save_cart_as_orders(user, customer, cart_items, tran_id='', payment_method='cod'):
    for item in cart_items:
        OrderPlaced.objects.create(
            user=user,
            customer=customer,
            fruit=item.fruit,
            quantity=item.quantity,
            tran_id=tran_id,
            payment_method=payment_method,
        )
        item.delete()


@login_required(login_url='/login/')
def initiate_payment(request):
    if request.method != 'POST':
        return redirect('checkout')

    user = request.user
    cart_items = list(Cart.objects.filter(user=user))
    if not cart_items:
        messages.error(request, 'Your cart is empty.')
        return redirect('showcart')

    address = CustomerAddress.objects.filter(
        id=request.POST.get('address_id'),
        user=user,
    ).first()
    if address is None:
        messages.error(request, 'Please select a valid delivery address.')
        return redirect('checkout')

    customer = _customer_for_order(user, address)
    payment_method = request.POST.get('payment_method', 'cod')

    # Cash on delivery never opens the payment gateway.
    if payment_method == 'cod':
        _save_cart_as_orders(user, customer, cart_items, payment_method='cod')
        messages.success(request, 'Order placed. Pay cash when the fruit is delivered.')
        return redirect('orders')

    amount = sum(
        (Decimal(str(item.fruit.discounted_price)) * item.quantity for item in cart_items),
        Decimal('0'),
    )
    total_amount = (amount + Decimal('100')).quantize(Decimal('0.01'))
    # SSLCommerz allows at most 30 characters. User and customer ids travel in value_a and value_b.
    tran_id = f"TXN{int(datetime.now().timestamp())}{uuid.uuid4().hex[:4]}"
    email = user.email if '@' in (user.email or '') else f'{user.username}@example.com'
    product_name = ', '.join(item.fruit.title for item in cart_items)[:255] or 'Fruits'

    sslcz = SSLCOMMERZ({
        'store_id': settings.SSLCZ_STORE_ID,
        'store_pass': settings.SSLCZ_STORE_PASS,
        'issandbox': settings.SSLCZ_IS_SANDBOX,
    })
    post_body = {
        'total_amount': f'{total_amount:.2f}',
        'currency': 'BDT',
        'tran_id': tran_id,
        'success_url': request.build_absolute_uri(reverse('payment_success')),
        'fail_url': request.build_absolute_uri(reverse('payment_fail')),
        'cancel_url': request.build_absolute_uri(reverse('payment_cancel')),
        'emi_option': 0,
        'cus_name': (customer.name or user.username)[:50],
        'cus_email': email[:50],
        'cus_phone': '01711111111',
        'cus_add1': (address.roadNumber or 'Dhaka')[:50],
        'cus_city': (address.district or 'Dhaka')[:50],
        'cus_state': (address.division or 'Dhaka')[:50],
        'cus_postcode': str(address.zipCode)[:30],
        'cus_country': 'Bangladesh',
        'shipping_method': 'NO',
        'num_of_item': len(cart_items),
        'product_name': product_name,
        'product_category': 'fruit',
        'product_profile': 'physical-goods',
        'value_a': str(user.id),
        'value_b': str(customer.id),
    }
    try:
        response = sslcz.createSession(post_body)
    except Exception:
        messages.error(request, 'Could not reach the payment gateway. Try again, or choose Cash on Delivery.')
        return redirect('checkout')
    if response.get('GatewayPageURL'):
        return redirect(response['GatewayPageURL'])

    reason = response.get('failedreason') or 'Payment session could not be created.'
    messages.error(request, reason)
    return redirect('checkout')


def _sslcommerz():
    return SSLCOMMERZ({
        'store_id': settings.SSLCZ_STORE_ID,
        'store_pass': settings.SSLCZ_STORE_PASS,
        'issandbox': settings.SSLCZ_IS_SANDBOX,
    })


def _payment_ids(data):
    user_id = str(data.get('value_a') or '')
    customer_id = str(data.get('value_b') or '')
    if user_id.isdigit() and customer_id.isdigit():
        return int(user_id), int(customer_id)
    parts = str(data.get('tran_id') or '').split('-')
    if len(parts) >= 3 and parts[1].isdigit() and parts[2].isdigit():
        return int(parts[1]), int(parts[2])
    return None, None


@csrf_exempt
def payment_success(request):
    data = request.POST or request.GET
    tran_id = data.get('tran_id', '')
    val_id = data.get('val_id', '')
    if data.get('status') not in ('VALID', 'VALIDATED') or not tran_id or not val_id:
        messages.error(request, data.get('error') or 'Payment was not confirmed.')
        return redirect('checkout')

    try:
        result = _sslcommerz().validationTransactionOrder(val_id)
    except Exception:
        messages.error(request, 'Could not verify the payment with SSLCommerz.')
        return redirect('checkout')

    if not result or result.get('status') not in ('VALID', 'VALIDATED') or result.get('tran_id') != tran_id:
        messages.error(request, 'SSLCommerz could not confirm this payment.')
        return redirect('checkout')

    user_id, customer_id = _payment_ids(result)
    if user_id is None:
        messages.error(request, 'Payment is missing the customer reference.')
        return redirect('checkout')

    try:
        user = User.objects.get(id=user_id)
        customer = Customer.objects.get(id=customer_id, user=user)
    except (User.DoesNotExist, Customer.DoesNotExist):
        messages.error(request, 'Could not match this payment to your account.')
        return redirect('checkout')

    cart_items = list(Cart.objects.filter(user=user))
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    if not cart_items:
        messages.info(request, f'Payment already recorded. Transaction ID: {tran_id}')
        return redirect('orders')

    expected = sum(
        (Decimal(str(item.fruit.discounted_price)) * item.quantity for item in cart_items),
        Decimal('0'),
    ) + Decimal('100')
    paid = Decimal(str(result.get('amount') or '0'))
    if paid != expected.quantize(Decimal('0.01')):
        messages.error(request, 'Paid amount does not match the cart total.')
        return redirect('checkout')

    _save_cart_as_orders(user, customer, cart_items, tran_id=tran_id, payment_method='bkash')
    messages.success(request, f'Payment successful. Transaction ID: {tran_id}')
    return redirect('orders')


@login_required(login_url='/login/')
def orders(request):
    order_list = OrderPlaced.objects.filter(user=request.user).select_related('fruit').order_by('-ordered_date')
    cart_count = Cart.objects.filter(user=request.user).count()
    return render(request, 'orders.html', {'orders': order_list, 'cart_count': cart_count})


@csrf_exempt
def payment_fail(request):
    reason = (request.POST or request.GET).get('error') or 'Payment failed. Please try again.'
    messages.error(request, reason)
    return redirect('checkout')


@csrf_exempt
def payment_cancel(request):
    messages.warning(request, "⚠️ Payment Cancelled by user.")
    return redirect('checkout')
