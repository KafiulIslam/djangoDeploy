from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from .models import Customer
from django.utils.translation import gettext, gettext_lazy as _


class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widget = {'username': forms.TextInput(attrs={'class': 'form-control'})}


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current_password', 'class': 'form-control'}))


# Customer form
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        form_control_attrs = {'class': 'form-control'}
        fields = ['name', 'division', 'district', 'thana', 'villorroad', 'zipcode']
        widgets = {'name': forms.TextInput(attrs=form_control_attrs),
                   'division': forms.Select(attrs=form_control_attrs),
                   'district': forms.TextInput(attrs=form_control_attrs),
                   'thana': forms.TextInput(attrs=form_control_attrs),
                   'villorroad': forms.TextInput(attrs=form_control_attrs),
                   'zipcode': forms.NumberInput(attrs=form_control_attrs)
                   }