from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView

from . import models


class ProductTypeView(ListView):
    model = models.ProductType



class ProductView(ListView):
    model = models.Product

    def get_queryset(self):
        product_type = self.kwargs.get('type')
        if product_type:
            return models.Product.objects.filter(type__name=product_type)
        return models.Product.objects.all()


