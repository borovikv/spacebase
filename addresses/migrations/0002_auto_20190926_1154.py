# Generated by Django 2.2.5 on 2019-09-26 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='country',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='street_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
