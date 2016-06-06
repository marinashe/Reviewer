from django import forms
from django.forms import formset_factory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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
            'description',
        )

    def add_feature(self, feature):
        self.fields["feature_{}".format(feature.id)] = forms.CharField(label=feature.name, max_length=100)


class CreateReviewForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = models.Review
        fields = (
            'text',
        )

    def add_score(self, score):
        self.fields["score_{}".format(score.id)] = forms.IntegerField(label=score.name)



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['name']

        if commit:
            user.save()
        models.UserProfile(user=user, id=user.id).save()

        return user
