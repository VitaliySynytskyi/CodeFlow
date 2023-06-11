# utils.py
import os
import requests

api_key = os.getenv('api_key')

def get_random_cat():
    response = requests.get(f'https://api.thecatapi.com/v1/images/search?api_key={api_key}')
    cat_data = response.json()
    return cat_data[0]['url']

def get_random_cat_fact():
    response = requests.get(f'https://catfact.ninja/fact')
    cat_data = response.json()
    return cat_data['fact']
