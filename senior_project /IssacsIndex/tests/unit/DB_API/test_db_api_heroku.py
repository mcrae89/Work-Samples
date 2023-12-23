import pytest
import os
import pytz
from datetime import datetime
from dotenv import load_dotenv
from unittest.mock import patch, MagicMock
import sys
sys.path.append('/home/meadnl89/SErepo/issacsindex')
from website.IssacsIndex_heroku import *
from DB_API.db_repo import *

load_dotenv()

identifier_to_test = "987456613274"
product_name_to_test = "Test Product"

@pytest.fixture(scope='function')
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    client = app.test_client()
    yield client

    # Cleanup created records to ensure isolation between tests
    with app.app_context():
        product = Product.query.filter_by(identifier=identifier_to_test).first()
        if product:
            Review.query.filter_by(product_id=product.id).delete()
            Price.query.filter_by(product_id=product.id).delete()
            Rating.query.filter_by(product_id=product.id).delete()
            
            db.session.delete(product)
            db.session.commit()
        db.session.remove()

def test_get_all_products(client):
    response = client.get('/products/')
    assert response.status_code == 200

def create_sample_product(client):
    payload = {
        "products": [
            {
            "identifier": "987456613274",
            "product_name": product_name_to_test,
            "product_description": "",
            "keywords": "",
            "issacs_insight": 0,
            "source_url": "https://www.example.com",
            "img": ""
            }
        ]
    }
    return client.post('/products/', json=payload)

def test_create_product(client):
    response = create_sample_product(client)
    assert response.status_code == 201

def test_create_product_with_invalid_data(client):
    # Missing required fields
    payload = {
        'issacs_insight': 40
    }
    response = client.post('/products/', json=payload)
    assert response.status_code == 400

def test_get_product_by_name(client):
    create_sample_product(client)
    response = client.get('/products/'+product_name_to_test)
    assert response.status_code == 200

def test_get_nonexistent_product(client):
    response = client.get('/products/nonexistent_identifier')
    assert response.status_code == 404

def test_update_product(client):
    create_sample_product(client)
    payload = {
        'issacs_insight': 100
    }
    response = client.put('/products/'+product_name_to_test, json=payload)
    assert response.status_code == 200

def test_update_nonexistent_product(client):
    payload = {
        'issacs_insight': 100
    }
    response = client.put('/products/nonexistent_identifier', json=payload)
    assert response.status_code == 404

def create_sample_reviews(client):
    payload = {
        "reviews": [
            {
                "product_name": product_name_to_test,
                "source": "TestUser1",
                "title" : "Test Reivew 1",
                "review": "This is the first test review.",
                "review_date": "2023-09-02T10:00:00"
            },
            {
                "product_name": product_name_to_test,
                "source": "TestUser2",
                "title": "Test Review 2",
                "review": "This is the second test review.",
                "review_date": "2023-10-20T00:00:00"
            }
        ]
    }
    return client.post('/reviews/', json=payload)

def test_create_reviews(client):
    create_sample_product(client)
    response = create_sample_reviews(client)
    assert response.status_code == 201

def test_create_review_for_nonexistent_product(client):
    payload = {
        "reviews": [
            {
                "product_name": "Nonexistent Product",
                "source": "TestUser1",
                "title": "Test Review 1",
                "review": "This is the first test review.",
                "review_date": "2023-10-19T00:00:00"
            },
            {
                "product_name": "Nonexistent Product",
                "source": "TestUser2",
                "title": "Test Review 2",
                "review": "This is the second test review.",
                "review_date": "2023-10-20T00:00:00"
            }
        ]
    }
    response = client.post('/reviews/', json=payload)
    assert response.status_code == 404

def test_get_reviews(client):
    create_sample_product(client)
    create_sample_reviews(client)
    response = client.get('/reviews/'+product_name_to_test)
    assert response.status_code == 200

def test_get_reviews_for_nonexistent_product(client):
    response = client.get('/reviews/nonexistent_identifier')
    assert response.status_code == 404

def create_sample_prices(client):
    payload = {
        "prices": [
            {
                "product_name": product_name_to_test,
                "price": 9.99,
                "price_url": "http://example.com/first",
                "retailer": "Test Retailer1"
            },
            {
                "product_name": product_name_to_test,
                "price": 19.99,
                "price_url": "http://example.com/second",
                "retailer": "Test Retailer2"
            }
        ]
    }
    return client.post('/prices/', json=payload)

def test_create_prices(client):
    create_sample_product(client)
    response = create_sample_prices(client)
    assert response.status_code == 201

def test_create_price_for_nonexistent_product(client):
    payload = {
        "prices": [
            {
                "product_name": "Nonexistent Product",
                "price": 9.99,
                "price_url": "http://example.com/first",
                "retailer": "Test Retailer1"
            },
            {
                "product_name": "Nonexistent Product",
                "price": 19.99,
                "price_url": "http://example.com/second",
                "retailer": "Test Retailer2"
            }
        ]
    }
    response = client.post('/prices/', json=payload)
    assert response.status_code == 404

def test_get_prices(client):
    create_sample_product(client)
    create_sample_prices(client)
    response = client.get('/prices/'+product_name_to_test)
    assert response.status_code == 200

def test_get_prices_for_nonexistent_product(client):
    response = client.get('/prices/nonexistent_identifier')
    assert response.status_code == 404

def create_sample_ratings(client):
    payload = {
        "ratings": [
            {
                "product_name": product_name_to_test,
                "avg_rating": 4.5,
                "number_of_ratings": 100
            },
            {
                "product_name": product_name_to_test,
                "avg_rating": 3.5,
                "number_of_ratings": 50
            }
        ]
    }
    return client.post('/ratings/', json=payload)

def test_create_ratings(client):
    create_sample_product(client)
    response = create_sample_ratings(client)
    assert response.status_code == 201

def test_create_rating_for_nonexistent_product(client):
    payload = {
        "ratings": [
            {
                "product_name": "Nonexistent Product",
                "avg_rating": 4.5,
                "number_of_ratings": 100
            },
            {
                "product_name": "Nonexistent Product",
                "avg_rating": 3.5,
                "number_of_ratings": 50
            }
        ]
    }
    response = client.post('/ratings/', json=payload)
    assert response.status_code == 404

def test_get_ratings(client):
    create_sample_product(client)
    create_sample_ratings(client)
    response = client.get('/ratings/'+product_name_to_test)
    assert response.status_code == 200

def test_get_ratings_for_nonexistent_product(client):
    response = client.get('/ratings/nonexistent_identifier')
    assert response.status_code == 404