from django.db import models
from django.contrib.auth.models import User

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    # Brand Model
    
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name



# Product

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    # Pricing
    mrp = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="MRP")
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Product info
    sku = models.CharField(max_length=100, unique=True, verbose_name="SKU")
    instock = models.BooleanField(default=True)
    return_available = models.BooleanField(default=True)

    # Age group choices
    AGE_CHOICES = [
        ('0-5m', '0-5 months'),
        ('5-8m', '5-8 months'),
        ('8-12m', '8-12 months'),
        ('1-2y', '1-2 years'),
        ('2-5y', '2-5 years'),
        ('5-8y', '5-8 years'),
        ('8-12y', '8-12 years'),
        ('12-14y', '12-14 years'),
    ]
    ages = models.CharField(max_length=10, choices=AGE_CHOICES, verbose_name="Age Group")

    # Delivery
    is_free_delivery = models.BooleanField(default=False)
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    is_new_arrival = models.BooleanField(default=False)

    # Inventory
    total_stock = models.PositiveIntegerField(default=100, verbose_name="Total Stock")
    stock_threshold = models.PositiveIntegerField(default=10, verbose_name="Low Stock Threshold")

    # Key features
    key_features = models.TextField(
        help_text="Enter key features separated by commas. Example: Durability, Safety, Lightweight"
    )
    description = models.TextField(blank=True, null=True)

    # Wholesale
    is_wholesale = models.BooleanField(default=False)
    min_wholesale_quantity = models.PositiveIntegerField(default=5)
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    sold_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_key_features(self):
        return [feature.strip() for feature in self.key_features.split(',') if feature.strip()]

    def save(self, *args, **kwargs):
        if self.is_free_delivery:
            self.delivery_charge = 0.00

        # Automatically update instock based on total stock
        self.instock = self.total_stock > 0

        super().save(*args, **kwargs)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # 1 to 5
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating})"        