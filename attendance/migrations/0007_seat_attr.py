# Generated by Django 4.2 on 2023-05-24 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_checksheet_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='attr',
            field=models.CharField(max_length=3, null=True),
        ),
    ]
