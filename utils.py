# utils.py
import requests

api_key = 'live_nh2nBNg7o0ezAaPFStcGG8LWXhJSSnDdezIO6YnqDlu4DxKSDjwyXY0hgnOLOe4k'

def get_random_cat():
    response = requests.get(f'https://api.thecatapi.com/v1/images/search?api_key={api_key}')
    cat_data = response.json()
    return cat_data[0]['url']

def get_random_cat_fact():
    response = requests.get(f'https://catfact.ninja/fact')
    cat_data = response.json()
    return cat_data['fact']
