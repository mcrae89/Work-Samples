import requests
import json
from backend.services.serp_api_service import SerpApiService
from backend.issacs_insight_score import IssacsInsightScore

class BuildProductPayload:
    def __init__(self, product_name, price, retailer_name, uri):
        self.product_name = product_name
        self.price = price
        self.retailer_name = retailer_name
        self.uri = uri
        self.serp_api_service = SerpApiService()
        self.issacs_insight_score = IssacsInsightScore()

    def _build_serp_api_package(self, product_name):
        serp_api_package = self.serp_api_service.fetch_product_details(product_name)
        product_id = ''
        for product in serp_api_package:
            if product.get('title') == product_name:
                product_id = product.get('product_id')
                break
        serp_api_reviews = []
        if product_id:
            serp_api_reviews = self.serp_api_service.fetch_product_reviews(product_id)
        return serp_api_package, serp_api_reviews

    def _build_issacs_insight_score(self, serp_api_package):
        products_payload = self.issacs_insight_score.calculate_issacs_insight_score(serp_api_package)
        return products_payload

    def _find_triggered_product_in_payload(self, products_payload, retailer_name):
        capitalized_retailer_name = retailer_name.title()

        for product in products_payload:
            product_source = product.get('source')
            if product_source and product_source.title() == capitalized_retailer_name:
                return product.get('position')

        return None


    def _format_updated_product_payload(self, products_payload, triggered_product_position):
        updated_product_payload = {}
        triggered_product_position = {
            'matched_triggered_product_position': triggered_product_position,
            'product_name': self.product_name,
            'price': self.price,
            'retailer_name': self.retailer_name,
            'uri': self.uri
        }
        updated_product_payload['triggered_product_position'] = triggered_product_position
        updated_product_payload['products'] = products_payload
        return updated_product_payload

    def _prep_payload_db(self, updated_products_payload, serp_api_reviews):
        product_db_payload = []
        price_db_payload = []
        ratings_db_payload = []
        reviews_db_payload = []

        for product in updated_products_payload['products']:
            # Extracting product details, with empty strings as defaults
            identifier = product.get('product_id', '')
            product_name = product.get('title', '')
            product_description = product.get('snippet', '')
            if product_description is None:
                product_description = ''
            keywords = product.get('extensions', '')
            if keywords is None:
                keywords = ''
            issacs_insight_score = product.get('final_issacs_insight_score', {}).get('final_issacs_insight_score', 0)
            if issacs_insight_score is None:
                issacs_insight_score = 0
            source_url = product.get('link', '').split('?')[0]
            img = product.get('thumbnail', '')

            # Product payload
            db_product_dict = {
                'identifier': identifier,
                'product_name': product_name,
                'product_description': product_description,
                'keywords': keywords,
                'issacs_insight': issacs_insight_score,
                'source_url': source_url,
                'img': img
            }
            product_db_payload.append(db_product_dict)

            # Price payload
            price = product.get('price', 0)
            if price is None:
                price = 0
            if price != 0:
                db_price_dict = {
                    'product_name': product_name,
                    'price': price,
                    'price_url': source_url,
                    'retailer': product.get('source')
                }
                price_db_payload.append(db_price_dict)

            # Ratings payload
            avg_rating = product.get('rating', 0)
            if avg_rating is None:
                avg_rating = 0
            number_of_ratings = product.get('reviews', 0)
            if number_of_ratings is None:
                number_of_ratings = 0
            if avg_rating != 0 or number_of_ratings != 0:
                db_ratings_dict = {
                    'product_name': product.get('title', ''),
                    'avg_rating': avg_rating if avg_rating is not None else 0,
                    'number_of_ratings': number_of_ratings if number_of_ratings is not None else 0
                }
                ratings_db_payload.append(db_ratings_dict)

        # Reviews payload
        if isinstance(serp_api_reviews, dict) and 'reviews' in serp_api_reviews:
            for review in serp_api_reviews['reviews']:
                product_name = review.get('product_name', '')
                if product_name is None:
                    product_name = ''
                source = review.get('source', '')
                if source is None: 
                    source = ''
                title = review.get('title', '')
                if title is None:
                    title = ''
                review_content = review.get('review', '')
                if review_content is None:
                    review_content = ''
                review_date = review.get('review_date', '')
                if review_date is None:
                    review_date = ''
                if product_name != '' and source != '' and review_content != '' and review_date != '':
                    db_reviews_dict = {
                        'product_name': product_name,
                        'source': source,
                        'title': title,
                        'review': review_content,
                        'review_date': review_date
                    }
                    reviews_db_payload.append(db_reviews_dict)
        elif isinstance(serp_api_reviews, list):
            for review in serp_api_reviews:
                product_name = review.get('product_name', '')
                if product_name is None:
                    product_name = ''
                source = review.get('source', '')
                if source is None: 
                    source = ''
                title = review.get('title', '')
                if title is None:
                    title = ''
                review_content = review.get('review', '')
                if review_content is None:
                    review_content = ''
                review_date = review.get('review_date', '')
                if review_date is None:
                    review_date = ''
                if product_name != '' and source != '' and review_content != '' and review_date != '':
                    db_reviews_dict = {
                        'product_name': product_name,
                        'source': source,
                        'title': title,
                        'review': review_content,
                        'review_date': review_date
                    }
                    reviews_db_payload.append(db_reviews_dict)
                    
        return product_db_payload, price_db_payload, ratings_db_payload, reviews_db_payload

    def _send_post_request(url, payload):
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=payload, headers=headers)
            response.raise_for_status()  # Raises HTTPError for bad status codes
            return response
        except requests.exceptions.HTTPError as errh:
            print(f"Http Error: {errh}")
            print(response.text)
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Request Error: {err}")

    def _persist_product_data(self, product_db_payload, price_db_payload, ratings_db_payload, reviews_db_payload):
        product_url = 'https://issacs-index-c54596d5a666.herokuapp.com/products/'
        price_url = 'https://issacs-index-c54596d5a666.herokuapp.com/prices/'
        ratings_url = 'https://issacs-index-c54596d5a666.herokuapp.com/ratings/'
        reviews_url = 'https://issacs-index-c54596d5a666.herokuapp.com/reviews/'

        serialized_product_payload = json.dumps({'products': product_db_payload})
        serialized_price_payload = json.dumps({'prices': price_db_payload})
        serialized_ratings_payload = json.dumps({'ratings': ratings_db_payload})
        serialized_reviews_payload = json.dumps({'reviews': reviews_db_payload})

        BuildProductPayload._send_post_request(product_url, serialized_product_payload)
        BuildProductPayload._send_post_request(price_url, serialized_price_payload)
        BuildProductPayload._send_post_request(ratings_url, serialized_ratings_payload)
        BuildProductPayload._send_post_request(reviews_url, serialized_reviews_payload)

    def get_products_payload(self):
        serp_api_package, serp_api_reviews = self._build_serp_api_package(self.product_name)
        products_payload = self._build_issacs_insight_score(serp_api_package)
        triggered_product_position = self._find_triggered_product_in_payload(products_payload, self.retailer_name)
        updated_products_payload = self._format_updated_product_payload(products_payload, triggered_product_position)
        product_db_payload, price_db_payload, ratings_db_payload, reviews_db_payload = self._prep_payload_db(updated_products_payload, serp_api_reviews)
        self._persist_product_data(product_db_payload, price_db_payload, ratings_db_payload, reviews_db_payload)

        return updated_products_payload, serp_api_reviews
