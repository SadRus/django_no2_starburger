import requests

from geocoder.models import Place


def fetch_coordinates(apikey, address):
    try:
        place, place_is_created = Place.objects.get_or_create(address=address)
        if place_is_created:
            base_url = 'https://geocode-maps.yandex.ru/1.x'
            response = requests.get(base_url, params={
                'geocode': address,
                'apikey': apikey,
                'format': 'json',
            })
            response.raise_for_status()

            found_places = response.json()['response']['GeoObjectCollection']['featureMember']
            most_relevant = found_places[0]
            lon, lat = most_relevant['GeoObject']['Point']['pos'].split(' ')
            place.longitude = lon
            place.latitude = lat
            place.save()
            return place.latitude, place.longitude
        return place.latitude, place.longitude
    except Exception:
        return None, None
