from django.db import models

STATUS_CHOICES = (
    ("Active", "Active"),
    ("Inactive", "Inactive")
)

ROLE_CHOICES = (
    ("Worker", "Worker"),
    ("Admin", "Admin")
)

# Create your models here.
class Member(models.Model):
    member_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.EmailField()
    hours_per_week = models.DecimalField(max_digits=4, decimal_places=1)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Active')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='Worker')
    

    def __str__(self):
        return f"{self.member_name}"