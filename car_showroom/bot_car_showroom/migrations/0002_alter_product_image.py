# Generated by Django 5.2.1 on 2025-05-25 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_car_showroom', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='products_data/nophoto.jpg', upload_to='products_data/'),
        ),
    ]
