# Generated by Django 3.2.4 on 2022-06-22 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productstemplate', '0005_alter_product_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('category', 'brand_name', 'product_name', 'specification')},
        ),
    ]
