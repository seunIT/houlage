# Generated by Django 2.0.7 on 2019-07-23 05:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Transport', '0020_remove_rent_driver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='pickup_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='rent',
            name='return_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
