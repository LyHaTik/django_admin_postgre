# Generated by Django 5.2.1 on 2025-05-25 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_car_showroom', '0002_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='products_data/nophoto.jpg', null=True, upload_to='products_data/'),
        ),
    ]
