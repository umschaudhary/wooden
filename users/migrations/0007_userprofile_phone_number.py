# Generated by Django 2.1.1 on 2018-11-23 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_userprofile_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(default='abc', error_messages={'max_length': 'Only 10 Digits Allowed'}, max_length=10),
            preserve_default=False,
        ),
    ]
