from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField
# Create your models here.
class Pastry(models.Model):
    image = models.ImageField(upload_to='pics')
    name= models.CharField(max_length=100)
    desc= models.TextField()
    price= models.IntegerField()
    offer= models.BooleanField(default=False)
    slug = models.SlugField()
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("pastryHome:checkout", kwargs={
            'slug': self.slug
        })
        
    def get_add_to_cart_url(self):
        return reverse("pastryHome:add_to_cart", kwargs={
            'slug': self.slug
        })
    
    def get_remove_from_cart_url(self):
        return reverse("pastryHome:remove_from_cart", kwargs={
            'slug': self.slug
        })

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=True)
    item = models.ForeignKey(Pastry, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"
    
    def get_total_item_price(self):
        return self.quantity * self.item.price
    def get_final_price(self):
        return self.get_total_item_price()
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing = models.ForeignKey('Billing', on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class Blogs(models.Model):
    imageDish = models.ImageField(upload_to = 'pics')
    imageUser = models.ImageField(upload_to = 'pics')
    userName = models.CharField(max_length=100)
    dateMonth = models.DateTimeField(auto_now=True)
    Heading = models.CharField(max_length = 100)
    desc= models.TextField()


class Billing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_Address = models.CharField(max_length=100)
    country = CountryField(multiple = False)
    zips = models.CharField(max_length=10)
    def __str__(self):
        return self.user.username
    
# class OrderUpdate(models.Model):
#     update_id = models.AutoField(primary_key=True)
#     order_id = models.IntegerField(default="")
#     update_desc = models.CharField(max_length=5000)
#     # timestamp = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.update_desc[0:15] + "...."