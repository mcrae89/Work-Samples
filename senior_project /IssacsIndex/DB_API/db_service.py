from .db_repo import *
from flask_restx import Api, Resource, fields

api = Api(version='1.0', title='Product API', description='A simple Product API',)

# Resources
ns_product = api.namespace('products', description='Product operations')
ns_review = api.namespace('reviews', description='Review operations')
ns_price = api.namespace('prices', description='Price operations')
ns_rating = api.namespace('ratings', description='Rating operations')

product_input = api.model('ProductInput', {
    'identifier': fields.String(required=True, description='identifier of the product'),
    'product_name': fields.String(required=True, description='Name of the product'),
    'product_description': fields.String(required=False, description='Description of the product'),
    'keywords': fields.String(required=False, description='Keywords of the product'),
    'issacs_insight': fields.Integer(required=False, description="Issac's Insight for the product"),
    'source_url': fields.String(required=True, description='Url of product being searched'),
    'img': fields.String(required=False, description='Image of product')
})

products_input = api.model('ProductsInput', {
    'products': fields.List(fields.Nested(product_input), required=True, description='List of Products')
})

product_input_for_update = api.model('ProductInputForUpdate', {
    'product_description': fields.String(required=False, description='Description of the product'),
    'keywords': fields.String(required=False, description='Keywords of the product'),
    'issacs_insight': fields.Integer(required=False, description="Issac's Insight for the product"),
    'source_url': fields.String(required=False, description='Url of product being searched'),
    'img': fields.String(required=False, description='Image of product')
})

review_input = api.model('ReviewInput', {
    'source': fields.String(required=True, description='Username of the reviewer and location of the review'),
    'title': fields.String(required = False, description='Title of the review'),
    'review': fields.String(required=True, description='Text of the review'),
    'review_date': fields.DateTime(required=True, description='Date of the review')
})

reviews_input = api.model('ReviewsInput', {
    'reviews': fields.List(fields.Nested(review_input), required=True, description='List of Reviews')
})

price_input = api.model('PriceInput', {
    'product_name': fields.String(required=True, description='Name of the product'),
    'price': fields.Float(required=True, description='Price of the product'),
    'price_url': fields.String(required=True, description='URL where the price is listed'),
    'retailer': fields.String(required=True, description='Retailer selling at this price')
})

prices_input = api.model('PricesInput', {
    'prices': fields.List(fields.Nested(price_input), required=True, description='List of Prices')
})

rating_input = api.model('RatingInput', {
    'avg_rating': fields.Float(required=True, description='Average rating of the product'),
    'number_of_ratings': fields.Integer(required=True, description='Number of users who rated the product')
})

ratings_input = api.model('RatingsInput', {
    'ratings': fields.List(fields.Nested(rating_input), required=True, description='List of Ratings')
})

@ns_product.route('/')
class ProductResource(Resource):
    @api.doc('get_all_products')
    def get(self):
        products = get_all_products()
        if products:
            return [product.serialize for product in products]
        return {"error": "No products found"}, 404

    @api.doc('create_multiple_products')
    @api.expect(products_input, validate=True)
    def post(self):
        data = api.payload['products']  # Access the list of products
        response_data = []

        for product_data in data:
            existing_product = get_product_by_name(product_data['product_name'])
            
            if existing_product:
                # Update the existing product
                updated_product = self.update_existing_product(existing_product, product_data)
                response_data.append({'updated': updated_product.serialize})
            else:
                # Add the new product
                new_product = self.add_new_product(product_data)
                response_data.append({'created': new_product.serialize})

        return response_data, 201
    
    def add_new_product(self, product_data):
        # Extract product details with defaults for optional fields
        issacs_insight = product_data.get('issacs_insight', None)
        img = product_data.get('img', None)
        product_description = product_data.get('product_description', None)
        keywords = product_data.get('keywords', None)

        # Add the new product
        return add_product(product_data['identifier'], product_data['product_name'],
                           product_description, keywords, issacs_insight, 
                           product_data['source_url'], img)

    def update_existing_product(self, existing_product, product_data):
        # Update fields of the existing product
        existing_product.product_description = product_data.get('product_description', existing_product.product_description)
        existing_product.keywords = product_data.get('keywords', existing_product.keywords)
        existing_product.issacs_insight = product_data.get('issacs_insight', existing_product.issacs_insight)
        existing_product.source_url = product_data.get('source_url', existing_product.source_url)
        existing_product.img = product_data.get('img', existing_product.img)

        # Save updates to the database
        return update_product_by_name(existing_product.product_name, existing_product.product_description, 
                                      existing_product.keywords, existing_product.issacs_insight, 
                                      existing_product.source_url, existing_product.img)

@ns_product.route('/<string:product_name>')
class ProductByproduct_nameResource(Resource):
    
    @api.doc('get_product')
    def get(self, product_name):
        product = get_product_by_name(product_name)
        if product:
            return product.serialize
        return {"error": "Product not found"}, 404
    
    @api.doc('update_product')
    @api.expect(product_input_for_update, validate=True)
    def put(self, product_name):
        data = api.payload
        product = get_product_by_name(product_name)
        if product is None:
            return {"error": "Product not found"}, 404
        
        if 'identifier' in data:
            return {"error": "Updating identifier is not allowed."}, 400
        if 'product_name' in data:
            return {"error": "Updating product_name is not allowed."}, 400

        if 'product_description' in data:
            product_description = data['product_description']
        else:
            product_description = product.product_description
        if 'keywords' in data:
            keywords = data['keywords']
        else:
            keywords = product.keywords
        if 'issacs_insight' in data:
            issacs_insight = data['issacs_insight']
        else:
            issacs_insight = product.issacs_insight
        if 'source_url' in data:
            source_url = data['source_url']
        else:
            source_url = product.source_url
        if 'img' in data:
            img = data['img']
        else:
            img = product.img
        
        updated_product = update_product_by_name(product_name, product_description, keywords, issacs_insight, source_url, img)
        if updated_product:
            return updated_product.serialize, 200
        return {"error": "Product not found"}, 404

@ns_review.route('/<string:product_name>')
class ReviewResource(Resource):
    @api.doc('get_reviews')
    def get(self, product_name):
        product = get_product_by_name(product_name)
        if product:
            reviews = get_reviews_by_similar_product_name(product_name)
            return reviews 
        else:
            return {"error": "Product not found"}, 404

@ns_review.route('/')
class CreateReviewResource(Resource):
    @api.doc('create_reviews')
    @api.expect(reviews_input, validate=True)
    def post(self):
        data = api.payload
        reviews_data = data.get('reviews')

        if not reviews_data:
            return {"error": "Reviews data is required in the payload"}, 400

        new_reviews = add_reviews_by_product_name(reviews_data)
        if new_reviews:
            return [review.serialize for review in new_reviews], 201
        else:
            return {"error": "No reviews were added"}, 404


@ns_price.route('/<string:product_name>')
class PriceResource(Resource):
    @api.doc('get_prices')
    def get(self, product_name):
        product = get_product_by_name(product_name)
        if product:
            prices = get_prices_by_similar_product_name(product_name)
            return prices 
        else:
            return {"error": "Product not found"}, 404

@ns_price.route('/')
class CreatePriceResource(Resource):
    @api.doc('create_prices')
    @api.expect(prices_input, validate=True)
    def post(self):
        data = api.payload
        prices_data = data.get('prices')
        
        # Check if prices data is provided
        if not prices_data:
            return {"error": "Prices data is required in the payload"}, 400

        new_prices = add_prices_by_product_name(prices_data)

        if new_prices:
            return [price.serialize for price in new_prices], 201
        else:
            return {"error": "No prices were added"}, 404
        
@ns_rating.route('/<string:product_name>')
class RatingResource(Resource):
    @api.doc('get_ratings')
    def get(self, product_name):
        product = get_product_by_name(product_name)
        if product:
            ratings = get_ratings_by_similar_product_name(product_name)
            return ratings 
        else:
            return {"error": "Product not found"}, 404

@ns_rating.route('/')
class CreateRatingResource(Resource):
    @api.doc('create_ratings')
    @api.expect(ratings_input, validate=True)
    def post(self):
        data = api.payload
        ratings_data = data.get('ratings')

        if not ratings_data:
            return {"error": "Ratings data is required in the payload"}, 400

        new_ratings = add_ratings_by_product_name(ratings_data)
        if new_ratings:
            return [rating.serialize for rating in new_ratings], 201
        else:
            return {"error": "No ratings were added"}, 404
