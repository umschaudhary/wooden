# Generated by Django 2.1.1 on 2018-11-22 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_userprofile_gender'),
        ('ratings', '0002_auto_20181122_1322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='guest_user',
        ),
        migrations.AddField(
            model_name='rating',
            name='guest_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.GuestEmail'),
        ),
    ]
