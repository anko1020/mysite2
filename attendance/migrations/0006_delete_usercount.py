# Generated by Django 4.2 on 2023-04-24 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_usercount'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserCount',
        ),
    ]
