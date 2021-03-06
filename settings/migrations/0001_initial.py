# Generated by Django 2.1.1 on 2018-11-01 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FiscalYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(error_messages={'max_length': 'Length Shouldnot exceed 64 Characters'}, max_length=64)),
                ('is_active', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Fiscal Year',
                'verbose_name_plural': 'Fiscal Years',
                'db_table': 'settings_fiscal_year',
            },
        ),
    ]
