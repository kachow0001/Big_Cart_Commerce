# Generated by Django 3.2.7 on 2023-09-03 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_address_zipcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='featured_product_id',
            field=models.IntegerField(null=True),
        ),
    ]
