# Generated by Django 3.1 on 2020-09-03 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_auto_20200903_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='images/&Y/&M/&D/'),
        ),
    ]