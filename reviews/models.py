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
    description = models.TextField(null=True, blank=True)
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    features = models.ManyToManyField(Feature, through='ProductFeature')

    def __str__(self):
        return self.name


class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)


class User(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Score(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Review(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000, null=True, blank=True)
    scores = models.ManyToManyField(Score, through='ReviewScore')


class ReviewScore(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    score = models.ForeignKey(Score, on_delete=models.CASCADE)
    value = models.IntegerField()