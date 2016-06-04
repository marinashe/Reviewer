from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name



class ProductType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Feature(models.Model):
    name = models.CharField(max_length=200)
    type = models.ForeignKey(ProductType)

    def __str__(self):
        return '{}({})'.format(self.name, self.type.name)


class Score(models.Model):
    name = models.CharField(max_length=200)
    type = models.ForeignKey(ProductType)

    def __str__(self):
        return '{}({})'.format(self.name, self.type.name)


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    features = models.ManyToManyField(Feature, through='ProductFeature')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("reviews:detail", args=(self.type.id, self.pk))


class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)


class Review(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile)
    text = models.CharField(max_length=2000, null=True, blank=True)
    scores = models.ManyToManyField(Score, through='ReviewScore')


class ReviewScore(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
    value = models.IntegerField()