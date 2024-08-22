from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

# user model 
class User(AbstractUser):
    language = models.CharField(default='english', max_length=30)
    pass

# Ticket
class Ticket(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateField()
    ticket_type = models.CharField(max_length=300)
    student = models.BooleanField(default=True)
    indian = models.BooleanField(default=True)
    paid = models.BooleanField(default=False)
    confirm = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is first created.
    age = models.IntegerField(validators=[MinValueValidator(6), MaxValueValidator(122)], null=True)
    total_cost = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)], null=True, blank=True)

    def total(self):
        # Ticket prices
        prices = {
            'general': {
                'Indian': 40,
                'Indian Student': 20,
                'Foreign Tourist': 300,
                'Foreign Student': 150
            },
            'composite': {
                'Indian': 300,
                'Indian Student': 40,
                'Foreign Tourist': 1000,
                'Foreign Student': 200
            },
            'night_visit': {
                'Indian': 100,
                'Indian Student': 100,
                'Foreign Tourist': 100,
                'Foreign Student': 100
            }
        }

        # Free entry days
        free_entry_days = ['30 March', '18 April', '18 May', '27 September']
        ticket_date = self.date.strftime('%d %B')
        if ticket_date in free_entry_days:
            return 0

        # Free entry for children below 7 years
        if not self.age and self.age < 7:
            return 0

        # Determine the visitor category
        if self.indian and self.student:
            category = 'Indian Student'
        elif self.indian:
            category = 'Indian'
        elif self.student:
            category = 'Foreign Student'
        else:
            category = 'Foreign Tourist'

        # Calculate the total cost based on ticket type
        total_cost = prices.get(self.ticket_type, {}).get(category,0)
        return total_cost
    
    def save(self, *args, **kwargs):
        self.total_cost = self.total()
        super().save(*args, **kwargs)
