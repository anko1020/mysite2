# Generated by Django 4.2 on 2023-06-08 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_sheetaccountrelation_back'),
    ]

    operations = [
        migrations.AddField(
            model_name='sheetaccountrelation',
            name='is_hold',
            field=models.BooleanField(default=False),
        ),
    ]