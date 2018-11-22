# Generated by Django 2.1.1 on 2018-11-22 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('items', '0008_auto_20181121_0004'),
    ]

    operations = [
        migrations.CreateModel(
            name='RefundPolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('validity', models.IntegerField()),
                ('cover', models.CharField(error_messages={'max_length': 'Should be of 160 Characters'}, max_length=160)),
                ('type_acceptance', models.CharField(error_messages={'max_length': 'Should be of 160 Characters'}, max_length=160)),
                ('description', models.TextField()),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='refunds', to='items.Item')),
            ],
            options={
                'db_table': 'refunds_refund_policy',
            },
        ),
    ]