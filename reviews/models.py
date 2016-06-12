from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)



class ProductType(models.Model):
    name = models.CharField(max_length=200)
    picture = models.ImageField( null=True, blank=True)

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

    def avg_score(self):
        sum = 0
        count = 0
        for r in Review.objects.filter(product=self):
            for s in ReviewScore.objects.filter(review=r):
                sum += int(s.value)
                count += 1
        return sum/count if count != 0 else 0


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
