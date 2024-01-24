# app.py (updated)
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to scrape weather information from Google search
def scrape_weather(city):
    try:
        url = f'https://www.google.com/search?q={city}+weather&hl=en&units=metric'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the relevant weather information
        temperature_element = soup.find('span', {'id': 'wob_tm'})
        condition_element = soup.find('span', {'id': 'wob_dc'})
        icon_element = soup.find('img', {'id': 'wob_tci'})
        city_element = soup.find('span', {'class': 'BBwThe'})

        # Check if the elements are present before accessing their text content
        if temperature_element and condition_element and icon_element and city_element:
            temperature = temperature_element.text
            condition = condition_element.text
            place = city_element.text
            icon_url = icon_element['src']

            return {'temperature': temperature, 'condition': condition, 'icon_url': icon_url, 'place': place}
        else:
            return {'error': 'Weather information not found'}

    except requests.exceptions.RequestException as e:
        return {'error': f'Error fetching data: {e}'}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        weather_info = scrape_weather(city)
        return render_template('index.html', weather_info=weather_info, city=city)

    return render_template('index.html', weather_info=None, city=None)

if __name__ == '__main__':
    app.run(debug=True)
