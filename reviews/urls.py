from django.conf.urls import url

from . import views
from . import models


app_name = "reviews"
urlpatterns = [
    url(r'^$', views.ProductTypeView.as_view(), name="type_list"),
    url(r'^(?P<pk>[0-9]+)$', views.ProductTypeDetailView.as_view(), name="product_list"),
    url(r'^(?P<type>[0-9]+)/add', views.ProductCreateView.as_view(), name="create_product"),
    url(r'^(?P<type>[0-9]+)/(?P<pk>[0-9]+)$', views.ProductDetail.as_view(), name="detail"),
    url(r'^user/(?P<pk>[0-9]+)$', views.UserProfileDetail.as_view(), name='profile_detail'),
    url(r'^user/create$', views.UserProfileCreate.as_view(), name='profile_create'),
]