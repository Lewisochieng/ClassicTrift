
from django.db import models
from django.template.context_processors import request
from django.contrib.auth.models import User


class Contact(models.Model):
        name = models.CharField(max_length=50)
        email = models.EmailField()
        phone = models.CharField(max_length=13)
        message = models.TextField()

        def __str__(self):
            return self.name

class Member(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')  # Main image

    # Add related products (self-referential ForeignKey)
    related_products = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        return self.name  # Image files are stored in the 'products/' directory


class ProductFeature(models.Model):
    product = models.ForeignKey(Product, related_name='features', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)  # Feature description

    def __str__(self):
        return f"{self.product.name} - {self.description}"


class AdditionalImage(models.Model):
    product = models.ForeignKey(Product, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/extra/')  # Path for additional images

    def __str__(self):
        return f"Extra Image for {self.product.name}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def total_price(self):
        return self.quantity * self.product.price