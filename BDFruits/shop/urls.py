from django.urls import path, reverse_lazy
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

# from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
                  path('', views.FruitListView.as_view(), name='fruit-list'),
                  path('fruit-details/<int:id>', views.FruitDetail.as_view(), name='fruit-detail'),
                  path('signup/', views.CustomRegistrationView.as_view(), name='signup'),
                  path('login/', views.CustomLoginView.as_view(), name='login'),
                  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
                  path('profile/', views.CustomerProfileView.as_view(), name='profile'),
                  path('address/', views.CustomerAddressView.as_view(), name='address'),
                  path('add-to-cart/<int:fruit_id>/', views.add_to_cart, name='add-to-cart'),
                  path('cart/', views.show_cart, name='showcart'),
                  path('checkout/', views.checkout, name='checkout'),

                  path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
                  path('payment/success/', views.payment_success, name='payment_success'),
                  path('payment/fail/', views.payment_fail, name='payment_fail'),
                  path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
                  path('orders/', views.orders, name='orders'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
