from django.db import models
from django.utils import timezone


class Place(models.Model):
    address = models.TextField('Адрес доставки', max_length=200, unique=True)
    longitude = models.FloatField(
        'Долгота',
        null=True,
        blank=True,
    )
    latitude = models.FloatField(
        'Широта',
        null=True,
        blank=True,
    )
    requested_at = models.DateTimeField(
        'Дата запроса к геокодеру',
        default=timezone.now,
    )

    def __str__(self):
        return self.address
