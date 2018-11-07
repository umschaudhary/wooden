# Generated by Django 2.1.1 on 2018-11-07 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_auto_20181107_1505'),
        ('companies', '0007_companyadmin_full_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ManyToManyField(related_name='company_categories', to='categories.Category')),
            ],
            options={
                'db_table': 'companies_company_category',
            },
        ),
    ]
