# Generated by Django 3.2.1 on 2021-06-30 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0016_auto_20210630_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubpost',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]