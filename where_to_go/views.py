from django.shortcuts import render, get_object_or_404
from places.models import Place
from django.http import JsonResponse
from django.urls import reverse


def start_page(request):
    places = Place.objects.all()
    
    features = []
    for place in places:
        detail_url = reverse(
            'place_detail',
            kwargs={'place_id': place.id}
        )
        
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.longitude, place.latitude]
            },
            "properties": {
                "title": place.title,
                "placeId": str(place.id),
                "detailsUrl": detail_url
            }
        }
        features.append(feature)
    
    places_geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    context = {
        'places_geojson': places_geojson,
    }
    
    return render(request, 'index.html', context=context)


def place_detail(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    
    image_urls = []
    images = place.images.all().order_by('order')
    for image in images:
        relative_url = image.image.url
        image_urls.append(relative_url)
    
    json_response = {
        "title": place.title,
        "imgs": image_urls,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lat": place.latitude,
            "lng": place.longitude
        }
    }
    
    response = JsonResponse(
        json_response,
        json_dumps_params={'ensure_ascii': False, 'indent': 2}
    )
    
    return response