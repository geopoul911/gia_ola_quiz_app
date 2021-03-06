# Generated by Django 2.1.15 on 2020-08-14 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200813_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
