from django.shortcuts import render
from django.contrib import messages
import requests
import datetime


def home(request):
    # Default city
    default_city = 'paris'
    city = request.POST.get('city', default_city)

    # OpenWeatherMap API configuration
    weather_api_key = '84638ef2622791028a0f4afc54dab1df' #api key
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric'

    # Google Custom Search API configuration
    search_api_key = 'AIzaSyDCMuRDr3fO_4Lt9y6w9OUkb9QQfNlYVLc' #your api key
    search_engine_id = '1638dbef97b074dc9' #engine id
    search_query = f"{city} 1920x1080"
    search_url = f"https://www.googleapis.com/customsearch/v1?key={search_api_key}&cx={search_engine_id}&q={search_query}&searchType=image&imgSize=xlarge"

    try:
        # Get weather data
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()  # Raise an error for bad responses
        weather_data = weather_response.json()
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()

    except (requests.exceptions.RequestException, KeyError) as e:
        # Handle errors in weather data fetching
        messages.error(request, 'Weather data is not available for the entered city.')
        description = 'clear sky'
        icon = '01d'
        temp = 25
        day = datetime.date.today()
        city = default_city
        exception_occurred = True

    else:
        exception_occurred = False

    try:
        # Get image data
        search_response = requests.get(search_url)
        search_response.raise_for_status()
        search_data = search_response.json()
        search_items = search_data.get("items")
        if search_items and len(search_items) > 1:
            image_url = search_items[1]['link']
        else:
            image_url = None

    except (requests.exceptions.RequestException, KeyError) as e:
        image_url = None  # or some default value

    # Render the template with the context data
    return render(request, 'weatherapp/index.html', {
        'description': description,
        'icon': icon,
        'temp': temp,
        'day': day,
        'city': city,
        'exception_occurred': exception_occurred,
        'image_url': image_url,
    })
