# Generated by Django 5.0.1 on 2024-09-24 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopreg',
            name='image',
            field=models.FileField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]
