# Generated by Django 4.2 on 2023-06-11 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_sheetaccountrelation_is_hold'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='earnings',
            field=models.IntegerField(default=0),
        ),
    ]