# Generated by Django 2.0 on 2018-02-01 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pvpstats', '0003_auto_20180130_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='pvpstats',
            name='number_matches',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pvpstats',
            name='kd',
            field=models.CharField(max_length=10),
        ),
    ]