from django.conf.urls import url

from . import views
from . import models


app_name = "reviews"
urlpatterns = [
    url(r'^$', views.ProductTypeView.as_view(), name="product_list"),
    url(r'^products/(?P<type>.*)', views.ProductView.as_view(), name="products"),

    ]