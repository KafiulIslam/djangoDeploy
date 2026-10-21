from django.urls import path, reverse_lazy
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

# from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    path('', views.FruitListView.as_view(), name='fruit-list'),
    # path('register/', views.CustomRegistrationView.as_view(), name='customerregistration'),
    #
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
