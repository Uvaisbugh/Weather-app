from django.contrib import messages
from django.shortcuts import render
import requests
import datetime

def home(request):
    if request.method == "POST":
        city = request.POST.get('city')
    else:
        city = 'London'
    
    # OpenWeatherMap API URL
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=c58c4d3e60c42917976fc78d05886296'
    PARAMS = {'units': 'metric'}
    
    # Google Custom Search API details for city image
    API_KEY = 'AIzaSyCqs59IeNdZdE17HawG8W6URwy1LtTo368'
    SEARCH_ENGINE_ID = 'e33dea6e7829f4869'
    query = city + " 1920x1080"
    search_type = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&searchType={search_type}&imgSize=xlarge"

    try:
        # Fetch weather data
        weather_data = requests.get(weather_url, params=PARAMS).json()
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()

        # Fetch city image
        image_data = requests.get(city_url).json()
        search_items = image_data.get("items")
        image_url = search_items[1]['link'] if search_items and len(search_items) > 1 else None

        return render(request, 'main.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })
    
    except (KeyError, IndexError, requests.RequestException) as e:
        # Set default values in case of any API error
        messages.error(request, 'City data is not available in the Weather API.')
        exception_occurred = True
        day = datetime.date.today()
        
        # Render default data in case of an error
        return render(request, 'main.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'Indore',
            'exception_occurred': exception_occurred,
            'image_url': 'https://defaultimageurl.com/default.jpg'  # Replace with a default image URL
        })
