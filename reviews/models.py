from django.db import models


class Feature(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=200)
    features = models.ManyToManyField(Feature)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    features = models.ManyToManyField(Feature, through='ProductFeature')


class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)
