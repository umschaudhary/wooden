# Generated by Django 2.1.1 on 2018-11-22 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refunds', '0004_auto_20181122_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refundrequest',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
