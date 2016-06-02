from django.conf.urls import url

from . import views
from . import models


app_name = "reviews"
urlpatterns = [
    url(r'^$', views.ProductTypeView.as_view(), name="type_list"),
    url(r'^(?P<type>[0-9]+)$', views.ProductView.as_view(), name="product_list"),
    url(r'^(?P<type>[0-9]+)/(?P<pk>[0-9]+)$', views.ProductDetail.as_view(), name="detail"),

]