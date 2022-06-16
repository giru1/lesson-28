from django.db import models

# Create your models here.


class Location(models.Model):
    name = models.CharField(max_length=150)
    lat = models.FloatField
    lng = models.FloatField

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'


class User(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    role = models.CharField(max_length=50)
    age = models.IntegerField(max_length=3)
    lat = models.FloatField
    lng = models.FloatField

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'