from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Product categories like Electronics, Clothing, etc."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    """A product in the store."""
    name        = models.CharField(max_length=200)
    description = models.TextField()
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    emoji       = models.CharField(max_length=10, default='📦')   # fun emoji icon
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    stock       = models.PositiveIntegerField(default=10)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def is_available(self):
        return self.stock > 0


class Order(models.Model):
    """An order placed by a user."""
    STATUS_CHOICES = [
        ('pending',    'Pending'),
        ('processing', 'Processing'),
        ('shipped',    'Shipped'),
        ('delivered',  'Delivered'),
    ]
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    def calculate_total(self):
        self.total = sum(item.subtotal for item in self.items.all())
        self.save()


class OrderItem(models.Model):
    """A single product line inside an order."""
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price    = models.DecimalField(max_digits=8, decimal_places=2)  # price at time of order

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def subtotal(self):
        return self.price * self.quantity
