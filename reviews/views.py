from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin

from . import models


class ProductTypeView(ListView):
    page_title = 'Unified Reviews System'
    model = models.ProductType


class ProductView(ListView):
    page_title = 'Products'
    model = models.Product

    def get_queryset(self):
        product_type = self.kwargs.get('type')
        if product_type:
            return models.Product.objects.filter(type__id=product_type)
        return models.Product.objects.all()


class ProductDetail(SingleObjectMixin, ListView):
    page_title = 'Reviews'
    template_name = 'reviews/product_detail.html'
    model = models.Review

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=models.Product.objects.filter(id=self.kwargs.get('pk')))
        return super(ProductDetail, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['product'] = self.object
        return context

    def get_queryset(self):
        return models.Review.objects.filter(product__id=self.object.id)


