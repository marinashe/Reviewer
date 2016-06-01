from django.conf.urls import url

from . import views


app_name = "expenses"
urlpatterns = [
    url(r'^$', views.ProductTypeView.as_view(), name="product_list"),

    ]