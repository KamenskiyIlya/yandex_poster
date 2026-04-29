from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from places.models import Place, PlaceImage


def start_page(request):
    places = Place.objects.all()

    features = []
    for place in places:
        detail_url = reverse('place_detail', kwargs={'place_id': place.id})

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [place.longitude, place.latitude],
            },
            'properties': {
                'title': place.title,
                'placeId': str(place.id),
                'detailsUrl': detail_url,
            },
        }
        features.append(feature)

    places_geojson = {'type': 'FeatureCollection', 'features': features}

    context = {
        'places_geojson': places_geojson,
    }

    return render(request, 'index.html', context=context)


def place_detail(request, place_id):
    place = get_object_or_404(
        Place.objects.prefetch_related(
            Prefetch('images', queryset=PlaceImage.objects.order_by('order'))
        ),
        id=place_id,
    )

    images = place.images.all()
    image_urls = [image.image.url for image in images]

    json_response = {
        'title': place.title,
        'imgs': image_urls,
        'short_description': place.short_description,
        'long_description': place.long_description,
        'coordinates': {'lat': place.latitude, 'lng': place.longitude},
    }

    response = JsonResponse(
        json_response, json_dumps_params={'ensure_ascii': False, 'indent': 2}
    )

    return response
