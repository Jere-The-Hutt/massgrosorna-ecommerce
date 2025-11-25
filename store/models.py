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
    author = models.CharField(max_length=200, blank=True, null=True)
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


class Order(models.Model):
    STATUS_CHOICES = (
        ('processing', 'Processing'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Store multiple product IDs as comma-separated string: "3,7,12"
    products = models.CharField(
        max_length=255,
        help_text="Comma-separated product IDs"
    )

    stripe_payment_intent = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    total_price = models.DecimalField(
        max_digits=7,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='processing'
    )

    shipping_name = models.CharField(max_length=200, blank=True, null=True)
    shipping_email = models.EmailField(blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"
