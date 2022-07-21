import re

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Car, Thing, Service, Seller, Picture
from django.forms.models import inlineformset_factory
import allauth.socialaccount.forms
import allauth.account.forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import TextInput
from django.contrib.postgres.forms import SimpleArrayField


class PhoneInput(TextInput):
    template_name = 'django/forms/widgets/phone_number.html'


User = get_user_model()


class SellerForm(ModelForm):
    """Form for seller editing"""
    class Meta:
        model = Seller
        fields = ['first_name', 'last_name', 'email', 'inn']


class UserSignupForm(forms.Form):
    """This form is for filling missing user profile data after signup"""
    first_name = forms.CharField(max_length=150, label='Имя')
    last_name = forms.CharField(max_length=150, label='Фамилия')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class UserProfileForm(forms.ModelForm):
    """This form is for editing user profile"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class CustomSimpleArrayField(SimpleArrayField):
    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split(',').strip()

    def validate(self, values):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(values)
        for tag in values:
            if not re.match(f'^[0-9a-zA-Z ]+$', tag):
                raise ValidationError(_('Validation error! Use only alphanumeric '
                                        + 'symbols for tags and comma as delimiter!'))


class AbstractAdForm(ModelForm):
    """Base class for common Ad objects methods and parameters"""
    tags = CustomSimpleArrayField(forms.CharField(max_length=50), delimiter=',')


class CarForm(AbstractAdForm):
    """This form is for creation and editing Car ads"""
    class Meta:
        model = Car
        fields = ['name', 'price', 'brand', 'mileage', 'color', 'description', 'category', 'tags']


class ThingForm(AbstractAdForm):
    """This form is for creation and editing Thing ads"""
    class Meta:
        model = Thing
        fields = ['name', 'price', 'weight', 'size', 'description', 'category', 'tags']


class ServiceForm(AbstractAdForm):
    """This form is for creation and editing Service ads"""
    class Meta:
        model = Service
        fields = ['name', 'price', 'area', 'description', 'category', 'tags']


class PictureForm(ModelForm):
    """This form is for adding pictures"""
    class Meta:
        model = Picture
        fields = ['pic']


class CustomSocialAccountSignupForm(allauth.socialaccount.forms.SignupForm):
    """This form is made for customizing oauth email validation"""
    def validate_unique_email(self, value):
        ret = super().validate_unique_email(value)
        if self.initial['email'] != value:
            raise forms.ValidationError(_('Email должен совпадать с данными вашего аккаунта соцсети'))
        return ret


class CustomAccountSignupForm(allauth.account.forms.SignupForm):
    """This form is made for customized user model signup"""
    phone_number = forms.IntegerField(max_value=999999999999, label='Номер телефона', widget=PhoneInput)


PictureFormset = inlineformset_factory(Car, Picture, form=PictureForm, extra=1)
