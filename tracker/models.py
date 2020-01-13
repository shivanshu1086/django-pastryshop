from django.db import models
from django.db.models import Model
from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from pastryHome.models import (Billing, Blogs, Pastry, Order, OrderItem)
# Create your models here.

class OrderUpdate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    Update_id = models.AutoField(primary_key = True)
    Order_id = models.IntegerField(default="")
    Update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.Update_desc[0:30] + "...."