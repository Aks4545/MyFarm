# Generated by Django 4.2.3 on 2023-07-24 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_userprofile_city_userprofile_latitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='longitude',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mobile_no',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
