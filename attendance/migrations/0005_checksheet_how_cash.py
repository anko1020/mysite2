# Generated by Django 4.2 on 2023-05-15 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_rename_seat_x_seat_pos_x_rename_seat_y_seat_pos_y'),
    ]

    operations = [
        migrations.AddField(
            model_name='checksheet',
            name='how_cash',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
