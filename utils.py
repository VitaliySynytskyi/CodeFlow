# utils.py
import os
import requests
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

api_key = os.getenv('api_key')

def get_random_cat():
    response = requests.get(f'https://api.thecatapi.com/v1/images/search?api_key={api_key}')
    cat_data = response.json()
    return cat_data[0]['url']

def get_random_cat_fact():
    response = requests.get(f'https://catfact.ninja/fact')
    cat_data = response.json()
    return cat_data['fact']

def authenticate_client():
    ta_credential = AzureKeyCredential(os.getenv('AzureKeyCredential'))
    text_analytics_client = TextAnalyticsClient(
            endpoint=os.getenv('endpoint'), 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

def sentiment_analysis_example(client, text):
    document = [text]
    response = client.analyze_sentiment(documents=document)[0]
    return response.sentiment