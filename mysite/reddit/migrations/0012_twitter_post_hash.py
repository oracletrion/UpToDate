# Generated by Django 2.0.3 on 2018-03-16 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reddit', '0011_auto_20180315_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitter_post',
            name='hash',
            field=models.CharField(default='', max_length=500),
        ),
    ]