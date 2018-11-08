# Generated by Django 2.1.1 on 2018-11-07 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_auto_20181107_2040'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='item_images', to='items.Item')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
                'db_table': 'items_item_image',
            },
        ),
    ]
