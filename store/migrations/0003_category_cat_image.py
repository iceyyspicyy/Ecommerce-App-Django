# Generated by Django 5.0.6 on 2024-06-13 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_category_options_product_is_sale_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='cat_image',
            field=models.ImageField(null=True, upload_to='uploads/category/'),
        ),
    ]
