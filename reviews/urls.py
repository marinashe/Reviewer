from django.conf.urls import url

from . import views
from . import models


app_name = "expenses"
urlpatterns = [
    url(r'^$', views.ProductTypeView.as_view(), name="product_list"),
    url(r'^product/(?P<type>.*)', views.ProductView.as_view(), name="product"),

    ]