# Generated by Django 3.2.4 on 2022-06-22 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productstemplate', '0006_alter_product_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
