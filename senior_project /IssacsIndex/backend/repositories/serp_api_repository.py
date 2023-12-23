import requests
from decouple import config

SERP_API_KEY = config('SERP_API_KEY') 

class SerpApiRepository:

    @classmethod
    def get_search_results_by_query(cls, query):
        url = "https://serpapi.com/search.json"
        params = {
            "api_key": SERP_API_KEY,
            "engine": "google_shopping",
            "google_domain": "google.com",
            "q": query,
            "num": 10
        }

        response = requests.get(url, params=params)
        data = response.json()
        return data
    
    @classmethod
    def get_reviews_by_product_id(cls, product_id):
        url = "https://serpapi.com/search.json"
        params = {
            "engine": "google_product",
            "product_id": product_id,
            "reviews": True,
            "gl": "us",
            "hl": "en",
            "api_key": SERP_API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()
        return data

#print(SerpApiRepository.get_search_results_by_query('Meta Quest 2'))