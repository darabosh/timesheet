# Generated by Django 4.1.3 on 2022-11-25 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
        ('clients', '0004_alter_client_client_name'),
        ('projects', '0008_remove_project_lead_project_lead'),
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Report',
            new_name='Timeslot',
        ),
    ]
