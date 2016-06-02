from django import forms
from . import models


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = (
            'name',
            'features',
        )

    # def __init__(self, *args, **kwargs):
    #     product_type = kwargs.get('type')
    #     super(CreateProductForm, self).__init__(*args, **kwargs)
    #     print(product_type)
    #     self.fields['features'].queryset = models.Feature.objects.filter(type=product_type)