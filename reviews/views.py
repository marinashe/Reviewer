from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView

from . import models


class ProductTypeView(ListView):
    page_title = 'Unified Reviews System'
    model = models.ProductType



class ProductView(ListView):
    page_title = 'Products'
    model = models.Product

    def get_queryset(self):
        product_type = self.kwargs.get('id')
        if product_type:
            return models.Product.objects.filter(type__id=product_type)
        return models.Product.objects.all()


class ReviewView(ListView):
    page_title = 'Reviews'
    model = models.Product

    def get_queryset(self):
        product_id = self.kwargs.get('id')
        if product_id:
            return models.Review.objects.filter(product__id=product_id)
        return models.Review.objects.all()


