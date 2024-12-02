from django.conf import settings
from django.contrib.auth.models import User
from django.db import models



class Passenger(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True, null=True)
    card_id = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=15)
    email = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    p_from = models.CharField(max_length=100, blank=True, null=True)
    p_to =models.CharField(max_length=100, blank=True, null=True)

class Passenger_Reg(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    category = models.CharField(max_length=100, default='General')  # Default for category
    package = models.CharField(max_length=100, default='Standard')  # Default for package



class Admin_Passenger_Reg(models.Model):
    card_id1 = models.CharField(max_length=50, blank=True, null=True)

   
class Children_form(models.Model):
    c_to = models.CharField(max_length=100)
    c_from = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Add price field

class ChildCard_form(models.Model):
    childName = models.CharField(max_length=100)
    childAddress = models.CharField(max_length=150)
    childMobile = models.CharField(max_length=15)

class Adults_form(models.Model):
    a_to = models.CharField(max_length=100)
    a_from = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Add price field

class AdultsCard_form(models.Model):
    adultsName = models.CharField(max_length=100)
    adultsAddress = models.CharField(max_length=150)
    adultsMobile = models.CharField(max_length=15)

class CombinedData(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    type = models.CharField(max_length=10)  # 'child' or 'adult'
    to_field = models.CharField(max_length=100, null=True, blank=True)
    from_field = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
   
    

class CryptoPayment(models.Model):
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id    