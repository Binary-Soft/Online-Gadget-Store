# Generated by Django 3.2.4 on 2022-07-13 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productstemplate', '0013_wishlist_lastdatatime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='lastdatatime',
            field=models.DateTimeField(),
        ),
    ]
