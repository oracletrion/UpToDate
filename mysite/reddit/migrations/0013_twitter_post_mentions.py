# Generated by Django 2.0.3 on 2018-03-16 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reddit', '0012_twitter_post_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitter_post',
            name='mentions',
            field=models.CharField(default='', max_length=2000),
        ),
    ]
