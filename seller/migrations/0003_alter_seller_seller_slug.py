# Generated by Django 4.2.3 on 2023-07-26 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0002_seller_seller_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='seller_slug',
            field=models.SlugField(blank=True, max_length=100),
        ),
    ]
