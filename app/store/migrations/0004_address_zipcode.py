# Generated by Django 3.2.7 on 2023-09-02 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='zipcode',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]