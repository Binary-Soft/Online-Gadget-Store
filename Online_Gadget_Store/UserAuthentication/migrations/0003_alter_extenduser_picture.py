# Generated by Django 4.0.4 on 2022-06-08 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAuthentication', '0002_alter_extenduser_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extenduser',
            name='picture',
            field=models.ImageField(default='default.webp', upload_to='userImages/'),
        ),
    ]