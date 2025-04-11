from django.db import models
from django.db.models import Avg

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.title


STARS = (
    (i, '* ' * i) for i in range(1, 6)
)

class Review(models.Model):
    text = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    stars = models.IntegerField(default=0, choices=STARS)


    def __str__(self):
        return self.text

    @property
    def average_rating(self):
        return self.stars.aggregate(avg=Avg('stars'))['avg'] or 0