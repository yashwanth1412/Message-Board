# Generated by Django 3.2.1 on 2021-06-21 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_post_liked_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(default='general', max_length=100),
        ),
    ]