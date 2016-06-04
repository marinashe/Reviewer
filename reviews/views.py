from django.contrib.auth import authenticate, logout, login
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, FormView, View
from django.views.generic.detail import SingleObjectMixin, DetailView

from . import models, forms


class LoggedInMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class LoginView(FormView):
    form_class = forms.LoginForm
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('reviews:type_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

        if user is not None and user.is_active:
            login(self.request, user)
            return redirect('reviews:type_list')

        form.add_error(None, "Invalid user name or password")
        return self.form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")


class ProductTypeView(LoggedInMixin, ListView):
    page_title = 'Unified Reviews System'
    model = models.ProductType

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductTypeDetailView(LoggedInMixin, DetailView):
    def page_title(self):
        return self.object
    model = models.ProductType

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    #
    # def get_queryset(self):
    #     product_type = self.kwargs.get('type')
    #     if product_type:
    #         return models.Product.objects.filter(type__id=product_type)
    #     return models.Product.objects.all()


class ProductDetail(LoggedInMixin, SingleObjectMixin, ListView):
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
        return models.Review.objects.filter(product__id=self.object.id).order_by('-time')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class ProductCreateView(LoggedInMixin, CreateView):
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
        form.instance.user = self.request.user
        return super().form_valid(form)

