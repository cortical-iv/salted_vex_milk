# Generated by Django 2.0 on 2017-12-18 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clans', '0003_auto_20171217_2346'),
    ]

    operations = [
        migrations.AddField(
            model_name='clan',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
