from django.db import models


class Place(models.Model):
    title = models.CharField(verbose_name='Название', unique=True)
    description_short = models.CharField(
        max_length=300, verbose_name='Короткое описание', blank=True
    )
    description_long = models.TextField(
        verbose_name='Полное описание', blank=True
    )
    longitude = models.FloatField(verbose_name='Долгота')
    latitude = models.FloatField(verbose_name='Широта')

    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(
        upload_to='place_images/',
        verbose_name='Изображение',
    )
    order = models.PositiveIntegerField(
        verbose_name='Порядок',
        default=0,
    )

    class Meta:
        ordering = ['order']
