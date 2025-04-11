from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class ApiUrls(models.Model):
    url = models.URLField()
    
    
    
    
    def __str__(self):
        return self.url


class Stadium(models.Model):
    name = models.CharField(max_length=255)
    location = models.URLField(max_length=255,null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True)  # This links to the User model
    price = models.DecimalField(max_digits=10, decimal_places=2,default=1)
    def __str__(self):
        return self.name

class Reservation(models.Model):
    stadium = models.ForeignKey(Stadium, related_name='reservations', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who made the reservation
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # The price for this reservation
    paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Set the total price based on the stadium's price when the reservation is created
        if not self.total_price:
            self.total_price = self.stadium.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reservation at {self.stadium.name} by {self.user.username}"


class Payment(models.Model):
    reservation = models.OneToOneField(Reservation, related_name='payment', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True, null=True)  # Allow null for existing rows
    payment_method = models.CharField(max_length=100,default='Unknown')
    payment_status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Payment of {self.amount} for Reservation {self.reservation.id}"



