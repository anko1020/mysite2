# Generated by Django 4.2 on 2023-05-07 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_fee', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=20, null=True)),
                ('client_num', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField(verbose_name='来店時間')),
                ('end_time', models.DateTimeField(verbose_name='退店時間')),
                ('start_overtime', models.CharField(max_length=20, null=True)),
                ('end_overtime', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Seat_ID', models.CharField(max_length=10, null=True)),
                ('is_use', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.client')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=20, null=True)),
                ('item_num', models.IntegerField()),
                ('item_cost', models.IntegerField()),
                ('checkSheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.checksheet')),
            ],
        ),
        migrations.AddField(
            model_name='checksheet',
            name='client',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='attendance.client'),
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_working', models.BooleanField(default=False)),
                ('start_time', models.DateTimeField(verbose_name='開始時間')),
                ('end_time', models.DateTimeField(verbose_name='終了時間')),
                ('start_overtime', models.CharField(max_length=20, null=True)),
                ('end_overtime', models.CharField(max_length=20, null=True)),
                ('is_sending', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
