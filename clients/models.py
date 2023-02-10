from django.db import models

# Create your models here.
COUNTRY_CHOICES = (
    ("us", "us"),
    ("uk", "uk"),
    ("serbia", "serbia"),
    ("china", "china"),
)

class Client(models.Model):
    client_name = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    zip = models.IntegerField()
    country = models.CharField(max_length=30, choices=COUNTRY_CHOICES, default="us")

    def __str__(self):
        return f"{self.client_name}"