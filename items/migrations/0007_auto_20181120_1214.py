# Generated by Django 2.1.1 on 2018-11-20 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_remove_item_in_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockrecord',
            name='discount_percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
    ]
