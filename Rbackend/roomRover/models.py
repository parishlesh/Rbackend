from django.contrib.auth.models import User
from django.db import models

class Room(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    description = models.TextField()
    parking_available = models.BooleanField(default=False)
    bachelors_allowed = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='room_pictures/', blank=True, null=True)
    contact = models.CharField(max_length=20, default='')    
    rent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.property_name + ' - ' + self.city + ', ' + self.state

