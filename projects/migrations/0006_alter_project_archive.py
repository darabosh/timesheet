# Generated by Django 4.1.3 on 2022-11-23 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_alter_project_archive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='archive',
            field=models.BooleanField(default=False),
        ),
    ]
