# Generated by Django 4.2 on 2023-05-16 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_checksheet_how_cash'),
    ]

    operations = [
        migrations.AddField(
            model_name='checksheet',
            name='staff',
            field=models.ManyToManyField(to='attendance.account'),
        ),
    ]
