# Generated by Django 4.2.3 on 2023-08-03 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_rename_item_orderedproduct_items'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderedproduct',
            old_name='items',
            new_name='products',
        ),
    ]