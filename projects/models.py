from django.db import models
from clients.models import Client
from members.models import Member

# Create your models here.
class Project(models.Model):
    project_name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=30)
    customer = models.ForeignKey(Client, on_delete=models.CASCADE)
    lead = models.ForeignKey(Member, on_delete=models.CASCADE)
    archive = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.project_name}"