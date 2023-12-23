import sys
sys.path.append('Q:\MSU\CS4360\senior-experience-group-project-issac-s-index')
sys.path.append('/home/meadnl89/SErepo/issacsindex')
from backend.repositories.serp_api_repository import SerpApiRepository

class SerpApiService:
    
    @staticmethod
    def fetch_product_details(query):
        raw_data = SerpApiRepository.get_search_results_by_query(query)
        
        products = raw_data.get('shopping_results', [])
        
        extracted_data = []
        for product in products:
            details = {
                "position": product.get('position', None),
                "title": product.get('title', None),
                "link": product.get('link', None),
                "product_id": product.get('product_id', None),
                "source": product.get('source', None),
                "price": product.get('extracted_price', None),
                "rating": product.get('rating', None),
                "reviews": product.get('reviews', None),
                "snippet": product.get('snippet', None),
                "thumbnail": product.get('thumbnail', None),
                "store_rating": product.get('store_rating', None),
                "store_reviews": product.get('store_reviews', None)
            }
            extracted_data.append(details) 
        
            
        return extracted_data
    
    @staticmethod
    def fetch_product_reviews(product_id):
        raw_data = SerpApiRepository.get_reviews_by_product_id(product_id)
        
        reviews = raw_data.get('reviews_results', {}).get('reviews', [])
        product_name = raw_data.get('product_results', {}).get('title', None)
        
        extracted_data = []
        for review in reviews:
            details = {
                "product_name": product_name,
                "position": review.get('position', None),
                "title": review.get('title', ''),
                "review_date": review.get('date', None),
                "rating": review.get('rating', None),
                "source": review.get('source', ''),
                "review": review.get('content', ''),
            }
            extracted_data.append(details)
        
        data_dict = {}
        data_dict['reviews'] = extracted_data
            
        return data_dict
    
#id = 14284785235002806804
#print(SerpApiService.fetch_product_reviews(id))