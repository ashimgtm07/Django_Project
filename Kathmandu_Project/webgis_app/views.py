from django.shortcuts import render
from django.http import JsonResponse
#from geopy.distance import geodesic
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geos import Point
from .models import MyLocation
import json
from pyproj import Transformer

def index(request):
    return render(request, 'webgis_app/index.html')

def map(request):
    return render(request, 'webgis_app/map.html')

def guidelines(request):
    return render(request, 'webgis_app/guidelines.html')

def about(request):
    return render(request, 'webgis_app/about.html')

def doc(request):
    return render(request, 'webgis_app/doc.html')

def fetch_hospitals(request):
    # Extract parameters from the request
    latitude = float(request.GET.get('latitude', 27.7))  # Default to Kathmandu's lat
    longitude = float(request.GET.get('longitude', 85.3))  # Default to Kathmandu's lon
    radius = float(request.GET.get('radius', 1000))  # Default radius: 1000 meters
    
    # Open the GeoJSON file
    try:
        with open('static/geojson/Ktm_Hospital.geojson', 'r', encoding='utf-8') as file:
            geojson_data = json.load(file)
            features = geojson_data['features']
            transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
            user_x, user_y = transformer.transform(longitude, latitude)

        
        # List of hospitals within the radius
        nearby_hospitals = []

        for feature in features:
            properties = feature.get('properties', {})
            geometry = feature.get('geometry', {}).get('coordinates', [])
            
            if geometry:
                lon, lat = geometry
                hospital_x, hospital_y = transformer.transform(lon, lat)

                # Calculate Euclidean distance in projected space (meters)
                distance = ((user_x - hospital_x)**2 + (user_y - hospital_y)**2)**0.5

                # Check if the hospital is within the specified radius
                if distance <= radius:
                    nearby_hospitals.append({
                        'name': properties.get('name', 'No Name'),
                        'type': properties.get('type', 'No Type'),
                        'location': [lat, lon],
                        'distance': distance  # Distance in meters
                    })

        return JsonResponse({'hospitals': nearby_hospitals})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def submit_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        lat = data.get('lat')
        lon = data.get('lon')

        if lat and lon:
            location = Point(float(lon), float(lat), srid=4326)
            MyLocation.objects.create(location=location)
            return JsonResponse({'message': 'Location saved successfully!'})
        else:
            return JsonResponse({'error': 'Invalid data'}, status=400)

