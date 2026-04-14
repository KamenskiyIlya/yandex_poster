from django.db import models


class Place(models.Model):
    title = models.CharField(verbose_name='Название')
    description_short = models.CharField(max_length=300, verbose_name='Короткое описание')
    description_long = models.TextField(verbose_name='Полное описание')
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    
    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='place_images/',
        verbose_name='Изображение',
    )
    order = models.PositiveIntegerField(verbose_name='Порядок')
    
    def __str__(self):
        return f'{self.order} {self.place.title}'