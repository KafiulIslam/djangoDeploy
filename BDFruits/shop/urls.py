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
                  # path('register/', views.CustomRegistrationView.as_view(), name='customerregistration'),
                  #
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
