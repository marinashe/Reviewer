from django import forms
from django.forms import formset_factory

from . import models

class ProductFeatureForm(forms.Form):
    feature = forms.CharField(max_length=200)
    value = forms.CharField(max_length=200)


FeaturesFormSet = formset_factory(ProductFeatureForm)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())


class CreateProductForm(forms.ModelForm):

    class Meta:
        model = models.Product
        fields = (
            'name',
            'features',
        )

