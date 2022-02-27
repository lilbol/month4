from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    @property
    def count_reviews(self):
        return self.reviews.all().count()

    @property
    def all_reviews(self):
        reviews = Review.objects.filter(product=self)
        return [{'id': i.id, 'text': i.text} for i in reviews]


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews')

    def __str__(self):
        return self.text
