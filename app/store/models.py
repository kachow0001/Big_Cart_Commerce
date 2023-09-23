from django.core.validators import MinValueValidator
from django.db import models

class Collection(models.Model):
    title = models.CharField(max_length=255)  # Fixed the field name from 'tittle' to 'title'
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='products')    
   
    class Meta:
        ordering = ['title']
        
        
    def __str__(self) -> str:
        return self.title  
    
      
class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True,blank=True)
    unit_price = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators= [MinValueValidator(1)]
    )  # Fixed the typo 'DecimaltField' to 'DecimalField'
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT,related_name='products')
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']

class Customer(models.Model):
    MEMBERSHIP_BASIC = 'B'
    MEMBERSHIP_DIAMOND = 'D'
    MEMBERSHIP_GOLD = 'G'
    
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BASIC, 'Basic'),
        (MEMBERSHIP_DIAMOND, 'Diamond'),
        (MEMBERSHIP_GOLD, 'GOLD')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    birth_date = models.DateTimeField(null=True)
    membership = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BASIC)
    
    def __str__(self):
        return  f'{self.first_name} {self.last_name}'
    
    class Meta:
        ordering = ['first_name','last_name']

class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]
    
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT,related_name='orderitems')
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)

class Cart(models.Model):  # Added a missing colon (:) at the end
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

