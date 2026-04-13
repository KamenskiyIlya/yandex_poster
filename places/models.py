from django.db import models

class Place(models.Model):
    title = models.CharField(verbose_name='Название')
    description_short = models.CharField(max_length=300, verbose_name='Короткое описание')
    description_long = models.TextField(verbose_name='Полное описание')
    latitude = models.FloatField(verbose_name='широта')
    longitude = models.FloatField(verbose_name='долгота')
    
    def __str__(self):
        return self.title

