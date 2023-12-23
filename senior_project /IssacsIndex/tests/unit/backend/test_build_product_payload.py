import pytest
import requests
import sys
sys.path.append('/home/meadnl89/SErepo/issacsindex')

from backend.builders.build_product_payload import BuildProductPayload

@pytest.fixture
def sample_products_package():
    return [
        {"position": 1, "title": "Star Wars Lightsaber", "link": "https://www.fake-starwars.com/lightsaber",
         "product_id": "SW123", "source": "Star Wars Shop", "price": 100.00, "rating": 1.0, "reviews": 100,
         "snippet": "A high-quality replica lightsaber", "thumbnail": "thumbnail_link_1", "store_rating": 2.0,
         "store_reviews": 2000},
        {"position": 2, "title": "Darth Vader Helmet", "link": "https://www.fake-starwars.com/vaderhelmet",
         "product_id": "DV456", "source": "Star Wars Shop", "price": 200.00, "rating": 3.0, "reviews": 300,
         "snippet": "Authentic Darth Vader helmet", "thumbnail": "thumbnail_link_2", "store_rating": 2.0,
         "store_reviews": 1500},
        {"position": 3, "title": "Millennium Falcon LEGO Set", "link": "https://www.fake-starwars.com/falconlego",
         "product_id": "MF789", "source": "Star Wars Shop", "price": 150.00, "rating": 5.0, "reviews": 500,
         "snippet": "Detailed LEGO set of Millennium Falcon", "thumbnail": "thumbnail_link_3", "store_rating": 5.0,
         "store_reviews": 2500}
    ]

@pytest.fixture
def sample_updated_products_payload():
    return [
        {
            'triggered_product_position': {
                'matched_triggered_product_position': 1,
                'product_name': 'Star Wars Lightsaber',
                'price': 100.0,
                'retailer_name': 'Star Wars Shop',
                'uri': 'https://www.fake-starwars.com/lightsaber'
            },
            'products': [{
                'position': 1,
                'title': 'Star Wars Lightsaber',
                'link': 'https://www.fake-starwars.com/lightsaber',
                'product_id': 'SW123',
                'source': 'Star Wars Shop',
                'price': 100.0,
                'rating': 1.0,
                'reviews': 100,
                'snippet': 'A high-quality replica lightsaber',
                'thumbnail': 'thumbnail_link_1',
                'store_rating': 2.0,
                'store_reviews': 2000,
                'insight_scores': {
                    'price_score': 133.33,
                    'rating_score': 20.0,
                    'reviews_score': 74.24,
                    'store_rating_score': 40.0,
                    'store_reviews_score': 97.15
                },
                'insight_score_weights': {
                    'price_score_weight': 0.25,
                    'rating_score_weight': 0.3,
                    'reviews_score_weight': 0.25,
                    'store_rating_score_weight': 0.1,
                    'store_reviews_score_weight': 0.1,
                    'total_weight': 1.0
                },
                'final_issacs_insight_score': {
                    'final_issacs_insight_score': 72
                }
            }, {
                'position': 2,
                'title': 'Darth Vader Helmet',
                'link': 'https://www.fake-starwars.com/vaderhelmet',
                'product_id': 'DV456',
                'source': 'StarWarsShop',
                'price': 200.0,
                'rating': 3.0,
                'reviews': 300,
                'snippet': 'Authentic Darth Vader helmet',
                'thumbnail': 'thumbnail_link_2',
                'store_rating': 2.0,
                'store_reviews': 1500,
                'insight_scores': {
                    'price_score': 66.67,
                    'rating_score': 60.0,
                    'reviews_score': 91.8,
                    'store_rating_score': 40.0,
                    'store_reviews_score': 93.47
                },
                'insight_score_weights': {
                    'price_score_weight': 0.25,
                    'rating_score_weight': 0.3,
                    'reviews_score_weight': 0.25,
                    'store_rating_score_weight': 0.1,
                    'store_reviews_score_weight': 0.1,
                    'total_weight': 1.0
                },
                'final_issacs_insight_score': {
                    'final_issacs_insight_score': 71
                }
            }, {
                'position': 3,
                'title': 'Millennium Falcon LEGO Set',
                'link': 'https://www.fake-starwars.com/falconlego',
                'product_id': 'MF789',
                'source': 'StarWarsShop',
                'price': 150.0,
                'rating': 5.0,
                'reviews': 500,
                'snippet': 'Detailed LEGO set of Millennium Falcon',
                'thumbnail': 'thumbnail_link_3',
                'store_rating': 5.0,
                'store_reviews': 2500,
                'insight_scores': {
                    'price_score': 100.0,
                    'rating_score': 100.0,
                    'reviews_score': 100.0,
                    'store_rating_score': 100.0,
                    'store_reviews_score': 100.0
                },
                'insight_score_weights': {
                    'price_score_weight': 0.25,
                    'rating_score_weight': 0.3,
                    'reviews_score_weight': 0.25,
                    'store_rating_score_weight': 0.1,
                    'store_reviews_score_weight': 0.1,
                    'total_weight': 1.0
                },
                'final_issacs_insight_score': {
                    'final_issacs_insight_score': 100
                }
            }]
        }
    ]

@pytest.fixture
def build_product_payload():
    product_name = "Some Product Name"
    price = 100.0
    retailer_name = "Some Retailer"
    uri = "http://example.com"

    return BuildProductPayload(product_name, price, retailer_name, uri)


def test_find_triggered_product_in_sample_package(build_product_payload, sample_products_package):
    # Arrange
    expected_result = 1
    retailer_name = "Star Wars Shop"

    # Act
    result = build_product_payload._find_triggered_product_in_payload(sample_products_package, retailer_name)

    # Assert
    assert isinstance(result, int)
    assert result == expected_result

def test_find_product_with_non_matching_retailer(build_product_payload, sample_products_package):
    # Arrange
    non_matching_retailer = "Unknown Retailer"

    # Act
    result = build_product_payload._find_triggered_product_in_payload(sample_products_package, non_matching_retailer)

    # Assert
    assert result is None

def test_find_product_with_case_insensitive_retailer(build_product_payload, sample_products_package):
    # Arrange
    case_insensitive_retailer = "star wars shop"

    # Act
    result = build_product_payload._find_triggered_product_in_payload(sample_products_package, case_insensitive_retailer)

    # Assert
    assert result is not None

def test_format_for_updated_product_payload(build_product_payload):
    # Arrange
    fake_triggered_product_position = 1
    fake_products_payload = [{"bigdata": "bigdata", "is": "is", "so": "cool"},
                             {"bigdata": "bigdata", "is": "is", "fake": "data"}]
    expected_result = {
        'triggered_product_position': {
            'matched_triggered_product_position': 1,
            'product_name': build_product_payload.product_name,
            'price': build_product_payload.price,
            'retailer_name': build_product_payload.retailer_name,
            'uri': build_product_payload.uri
        },
        'products': fake_products_payload
    }

    # Act
    result = build_product_payload._format_updated_product_payload(fake_products_payload, fake_triggered_product_position)

    # Assert
    assert isinstance(result, dict)
    assert result == expected_result

def test_prep_payload_db(build_product_payload, sample_updated_products_payload):
    # Act
    product_db_payload, price_db_payload, ratings_db_payload = build_product_payload._prep_payload_db(sample_updated_products_payload)

    # Assert
    assert isinstance(product_db_payload, list)
    assert isinstance(price_db_payload, list)
    assert isinstance(ratings_db_payload, list)

def test_send_post_request(monkeypatch, build_product_payload):
    # Arrange
    def mock_post(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        response._content = b'{"key": "value"}'
        return response

    monkeypatch.setattr(requests, "post", mock_post)
    url = "http://example.com/api"
    payload = {"key": "value"}

    # Act
    response = BuildProductPayload._send_post_request(url, payload)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"key": "value"}