# Generated by Django 4.2 on 2023-05-14 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='checksheet',
            name='memo_str',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
