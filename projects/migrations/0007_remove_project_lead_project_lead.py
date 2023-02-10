# Generated by Django 4.1.3 on 2022-11-24 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
        ('projects', '0006_alter_project_archive'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='lead',
        ),
        migrations.AddField(
            model_name='project',
            name='lead',
            field=models.ManyToManyField(to='members.member'),
        ),
    ]
