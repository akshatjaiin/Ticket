from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

class User(AbstractUser):
    pass

# Ticket
class Ticket(models.Model):
    name = models.CharField(max_length=30)
    date = models.CharField(max_length=30)
    ticket_type = models.CharField(max_length=300)
    student = models.BooleanField(default=True)
    indian = models.BooleanField(default=True)
    paid = models.BooleanField(default=False)
    confirm = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is first created.
    age = models.IntegerField(validators=[MinValueValidator(6), MaxValueValidator(122)], null=True)
    
