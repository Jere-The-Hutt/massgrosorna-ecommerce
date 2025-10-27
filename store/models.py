from django.db import models
from django.contrib.auth.models import User


# Optional Category model (future-proof)
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
        )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2
        )
    image1 = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
        )
    image2 = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
        )
    image3 = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
        )

    def __str__(self):
        return self.title
