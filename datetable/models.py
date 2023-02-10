from django.db import models
from clients.models import Client
from projects.models import Project
from members.models import Member

class Timeslot(models.Model):
    date = models.DateField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    time = models.DecimalField(max_digits=3, decimal_places=1)
    overtime = models.DecimalField(max_digits=3, decimal_places=1)
    