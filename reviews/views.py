from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView
from django.views.generic.detail import SingleObjectMixin, DetailView

from . import models, forms


class ProductTypeView(ListView):
    page_title = 'Unified Reviews System'
    model = models.ProductType


class ProductTypeDetailView(DetailView):
    def page_title(self):
        return self.object
    model = models.ProductType
    #
    # def get_queryset(self):
    #     product_type = self.kwargs.get('type')
    #     if product_type:
    #         return models.Product.objects.filter(type__id=product_type)
    #     return models.Product.objects.all()


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


class ProductCreateView(CreateView):
    form_class = forms.CreateProductForm
    template_name = "reviews/product_form.html"

    success_url = reverse_lazy('reviews:product_list')

    def dispatch(self, request, *args, **kwargs):
        self.type = get_object_or_404(models.ProductType, id=kwargs['type'])
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['features'].queryset = models.Feature.objects.filter(type=self.type)
        return form

    def form_valid(self, form):
        form.instance.type = self.request.type
        return super().form_valid(form)


