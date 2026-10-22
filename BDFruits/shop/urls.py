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
                  path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
                  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
                  # path('register/', views.CustomRegistrationView.as_view(), name='customerregistration'),
                  #
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
