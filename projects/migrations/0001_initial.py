# Generated by Django 4.1.3 on 2022-11-22 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=30)),
                ('customer', models.CharField(max_length=30)),
                ('lead', models.CharField(max_length=30)),
            ],
        ),
    ]
