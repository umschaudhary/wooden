# Generated by Django 2.1.1 on 2018-11-20 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='Order',
            new_name='order',
        ),
    ]
