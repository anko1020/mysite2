# Generated by Django 4.2 on 2023-05-15 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_seat_seat_x_seat_seat_y'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seat',
            old_name='seat_x',
            new_name='pos_x',
        ),
        migrations.RenameField(
            model_name='seat',
            old_name='seat_y',
            new_name='pos_y',
        ),
    ]