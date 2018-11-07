# Generated by Django 2.1.1 on 2018-11-07 03:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_auto_20181101_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyadmin',
            name='email',
            field=models.EmailField(default='ums@gmail.com', max_length=254, validators=[django.core.validators.EmailValidator(message='Invalid Email Address')]),
            preserve_default=False,
        ),
    ]
