# Generated by Django 2.0 on 2017-12-17 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clans', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clan',
            old_name='group_id',
            new_name='clan_id',
        ),
        migrations.AddField(
            model_name='clan',
            name='call_sign',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='clan',
            unique_together={('name', 'clan_id')},
        ),
    ]
