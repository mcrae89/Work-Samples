from datetime import datetime
import pytz
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields
from dotenv import load_dotenv
import os
import requests
import subprocess
import json
from DB_API.db_service import *
from backend.builders.build_product_payload import BuildProductPayload

load_dotenv()

app = Flask(__name__, static_folder='static')

# Database configurations
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db.init_app(app)
@app.route('/')
def homepage():
    return render_template("home_page.html")

api.init_app(app)

# API Base URL for IssacsIndex
API_BASE_URL = os.environ.get('API_BASE_URL')

@app.teardown_appcontext
def teardown_session(exception=None):
    if exception:
        db.session.rollback()
    else:
        db.session.commit()
    db.session.remove()

def get_product_by_name(product_name):
    response = requests.get(f"{API_BASE_URL}/products/{product_name}")
    if response.status_code == 200:
        return response.json()
    return None

def get_reviews_by_name(product_name):
    response = requests.get(f"{API_BASE_URL}/reviews/{product_name}")
    if response.status_code == 200:
        reviews_data = response.json()

        # Process each review
        for review_data in reviews_data:
            review = review_data['review']  # Access the nested review dictionary
            review_date_str = review.get('review_date')

            if review_date_str:
                if '.' in review_date_str:
                    format_str = "%Y-%m-%dT%H:%M:%S.%f"
                else:
                    format_str = "%Y-%m-%dT%H:%M:%S"
                review_date_datetime = datetime.strptime(review_date_str, format_str)

                # Format the datetime object to a string and update the review_date in the nested dictionary
                review['review_date'] = review_date_datetime.strftime("%m/%d/%Y")

        return reviews_data
    return []

def get_prices_by_name(product_name):
    response = requests.get(f"{API_BASE_URL}/prices/{product_name}")
    if response.status_code == 200:
        return response.json()
    return []

def convert_utc_to_local(utc_datetime):
    # utc_datetime is a datetime object
    utc_datetime = utc_datetime.replace(tzinfo=pytz.UTC)
    local_timezone = pytz.timezone('America/Denver')
    local_datetime = utc_datetime.astimezone(local_timezone)
    return local_datetime

@app.route('/product/<product_name>')
def review_page(product_name):
    product = get_product_by_name(product_name)

    if product is None:
        return "Product not found", 404
    
    reviews = get_reviews_by_name(product_name)
    prices = get_prices_by_name(product_name)

    # Handle potential datetime strings with or without milliseconds
    if '.' in product['last_updated_date']:
        format_str = "%Y-%m-%dT%H:%M:%S.%f"
    else:
        format_str = "%Y-%m-%dT%H:%M:%S"
    date = datetime.strptime(product['last_updated_date'], format_str)
    localDate = convert_utc_to_local(date)

    return render_template(
        "reviews.html",
        date=localDate,
        product=product,
        reviews=reviews,
        prices=prices
    )

@app.route('/scrape', methods=['GET'])
def scrape():
    # Get the URL parameter from the request
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    # Call the Node.js script with the URL
    result = subprocess.run(['node', '/app/chrome_extension/product-scraper-v2.js', url], capture_output=True, text=True)

    # Check for errors
    if result.returncode != 0:
        return jsonify({"error": "Failed to run the scraper", "details": result.stderr}), 500

    # Parse and return the output
    try:
        data = json.loads(result.stdout)
        return jsonify(data)
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse scraper output", "details": result.stdout}), 500
    
@app.route('/ce/trigger-product-data', methods=['POST'])
def trigger_product_data():
    data = request.json
    
    required_keys = ['product_name', 'price', 'retailer_name']
    for key in required_keys:
        if key not in data:
            return jsonify({'error': 'Missing data'}), 400

    product_name = data['product_name']
    price = data['price']
    retailer_name = data['retailer_name']
    uri = data['uri']

    build_product_payload = BuildProductPayload(product_name, price, retailer_name, uri)
    payload = build_product_payload.get_products_payload()

    return jsonify(payload), 200

if __name__ == "__main__":
    app.run(debug=True)