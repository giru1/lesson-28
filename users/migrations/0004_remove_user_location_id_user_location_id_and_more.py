# Generated by Django 4.0.5 on 2022-06-19 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_location_lat_location_lng'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='location_id',
        ),
        migrations.AddField(
            model_name='user',
            name='location_id',
            field=models.ManyToManyField(to='users.location'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('member', 'Пользователь'), ('moderator', 'Модератор'), ('admin', 'Админ')], default='member', max_length=50),
        ),
    ]