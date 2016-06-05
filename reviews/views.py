from django.contrib.auth import authenticate, logout, login
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
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
    page_title = 'Login'

    form_class = forms.LoginForm
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        self.redirect_to = request.GET['next']
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

        if user is not None and user.is_active:
            login(self.request, user)
            return HttpResponseRedirect(self.redirect_to)

        form.add_error(None, "Invalid user name or password")
        return self.form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("reviews:type_list")


class ProductTypeView(ListView):
    page_title = 'Unified Reviews System'
    model = models.ProductType

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductTypeDetailView(DetailView):
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
        return models.Review.objects.filter(product__id=self.object.id).order_by('-time')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def foo(self, x):
        return "xxx"


class ProductCreateView(LoggedInMixin, CreateView):
    page_title = 'Add Product'

    form_class = forms.CreateProductForm
    template_name = "reviews/product_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.producttype = get_object_or_404(models.ProductType, id=kwargs['type'])
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for feature in models.Feature.objects.filter(type=self.producttype):
            form.add_feature(feature)
        return form

    def form_valid(self, form):

        form.instance.type = self.producttype
        form.instance.user = self.request.user

        resp = super().form_valid(form)

        for f in models.Feature.objects.filter(type=form.instance.type):
            models.ProductFeature.objects.create(
                product=form.instance,
                value=form.cleaned_data['feature_{}'.format(f.id)],
                feature=f,
            )
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('reviews:product_list', kwargs={'pk': self.producttype.pk})


class UserProfileDetail(DetailView):
    model = models.UserProfile


class UserProfileCreate(CreateView):
    form_class = forms.RegistrationForm
    template_name = "reviews/userprofile_form.html"

    def form_valid(self, form):
        self.username = form.cleaned_data['username']
        self.password = form.cleaned_data['password1']

        return super().form_valid(form)

    def get_success_url(self):
        user = authenticate(username=self.username, password=self.password)
        login(self.request, user)
        return reverse_lazy('reviews:type_list')


class ReviewCreateView(LoggedInMixin, CreateView):
    page_title = 'Add Review'

    form_class = forms.CreateReviewForm
    template_name = "reviews/review_form.html"


    def dispatch(self, request, *args, **kwargs):
        self.producttype = get_object_or_404(models.ProductType, id=kwargs['type'])
        self.productid = get_object_or_404(models.Product, id=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for score in models.Score.objects.filter(type=self.producttype):
            form.add_score(score)
        return form

    def form_valid(self, form):
        form.instance.product = self.productid
        form.instance.user = models.UserProfile.objects.filter(user=self.request.user)[0]

        resp = super().form_valid(form)

        for f in models.Score.objects.filter(type=self.producttype):
            models.ReviewScore.objects.create(
                review=form.instance,
                value=form.cleaned_data['score_{}'.format(f.id)],
                score=f,
            )
        return resp

    def get_success_url(self, **kwargs):
        return reverse_lazy('reviews:detail', kwargs={'type': self.producttype.pk, 'pk': self.productid.id})

