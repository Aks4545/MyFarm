# Generated by Django 3.1 on 2023-07-22 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20230722_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveIntegerField(choices=[(1, 'Vendor'), (2, 'Customer')]),
        ),
    ]
