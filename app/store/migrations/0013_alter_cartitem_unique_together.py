# Generated by Django 3.2.7 on 2023-10-12 23:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_auto_20231012_2322'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('cart', 'product')},
        ),
    ]
