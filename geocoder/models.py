from django.db import models
from django.utils import timezone


class Place(models.Model):
    address = models.TextField('Адрес доставки', max_length=200)
    longitude = models.FloatField(
        'Долгота',
    )
    latitude = models.FloatField(
        'Широта',
    )
    requested_at = models.DateTimeField(
        'Дата запроса к геокодеру',
        default=timezone.now(),
    )
