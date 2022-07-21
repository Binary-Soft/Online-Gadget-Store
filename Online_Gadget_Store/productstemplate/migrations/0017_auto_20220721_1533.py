# Generated by Django 3.2.4 on 2022-07-21 09:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productstemplate', '0016_alter_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeadLineMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=30)),
                ('logo', models.ImageField(upload_to='HeadLine', verbose_name='Picture')),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(default=0.0, help_text='Price Can not be Less than Zero.', validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
