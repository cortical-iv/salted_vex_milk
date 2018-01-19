# Generated by Django 2.0 on 2018-01-02 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0013_member_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='clan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clans.Clan'),
        ),
    ]