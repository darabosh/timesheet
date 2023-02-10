# Generated by Django 4.1.3 on 2022-11-22 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_alter_client_address_alter_client_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='country',
            field=models.CharField(choices=[('us', 'us'), ('uk', 'uk'), ('serbia', 'serbia'), ('china', 'china')], default='us', max_length=30),
        ),
    ]