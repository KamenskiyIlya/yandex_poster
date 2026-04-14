from django.shortcuts import render
from places.models import Place


def start_page(request):
    places = Place.objects.all()
    
    features = []
    for place in places:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.longitude, place.latitude]
            },
            "properties": {
                "title": place.title,
                "placeId": str(place.id),
                "detailsUrl": f'static/places/{place.id}.json'
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