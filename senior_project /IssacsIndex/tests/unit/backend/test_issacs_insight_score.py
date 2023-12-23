import pytest
import numpy as np
import sys
sys.path.append('/home/meadnl89/SErepo/issacsindex')
from backend.issacs_insight_score import IssacsInsightScore

@pytest.fixture
def sample_products_package():
    return [
        {"position": 1, "title": "Star Wars Lightsaber", "link": "https://www.fake-starwars.com/lightsaber",
         "product_id": "SW123", "source": "StarWarsShop", "price": 100.00, "rating": 1.0, "reviews": 100,
         "snippet": "A high-quality replica lightsaber", "thumbnail": "thumbnail_link_1", "store_rating": 2.0,
         "store_reviews": 2000},
        {"position": 2, "title": "Darth Vader Helmet", "link": "https://www.fake-starwars.com/vaderhelmet",
         "product_id": "DV456", "source": "StarWarsShop", "price": 200.00, "rating": 3.0, "reviews": 300,
         "snippet": "Authentic Darth Vader helmet", "thumbnail": "thumbnail_link_2", "store_rating": 2.0,
         "store_reviews": 1500},
        {"position": 3, "title": "Millennium Falcon LEGO Set", "link": "https://www.fake-starwars.com/falconlego",
         "product_id": "MF789", "source": "StarWarsShop", "price": 150.00, "rating": 5.0, "reviews": 500,
         "snippet": "Detailed LEGO set of Millennium Falcon", "thumbnail": "thumbnail_link_3", "store_rating": 5.0,
         "store_reviews": 2500}
    ]

@pytest.fixture
def empty_products_package():
    return []

@pytest.fixture
def null_values_products_package():
    return [
        {"title": "X-Wing Model", "price": 100.00, "rating": 4.2, "reviews": 450, "store_rating": 4.5,
         "store_reviews": 1000},
        {"title": "TIE Fighter Toy", "price": None, "rating": 4.1, "reviews": 300, "store_rating": 4.4,
         "store_reviews": 900},
        {"title": "Rebel Pilot Helmet", "price": 200.00, "rating": None, "reviews": None, "store_rating": 4.3,
         "store_reviews": 800},
        {"title": "Stormtrooper Armor", "price": None, "rating": 3.8, "reviews": 550, "store_rating": None,
         "store_reviews": None},
        {"title": "Chewbacca Plush", "price": None, "rating": None, "reviews": None, "store_rating": 4.2,
         "store_reviews": None},
        {"title": "Death Star Planter", "price": None, "rating": None, "reviews": None, "store_rating": None,
         "store_reviews": None}
    ]

@pytest.fixture
def insight_score():
    return IssacsInsightScore()


# _calculate_average_price()

def test_verify_average_price_calculation(sample_products_package):
    # Arrange
    expected_average = 150.00

    # Act
    calculated_average = IssacsInsightScore._find_average_price(sample_products_package)

    # Assert
    assert calculated_average == pytest.approx(expected_average)

# _calculate_price_score()

def test_verify_price_score_calculation(sample_products_package):
    # Arrange
    product_price = sample_products_package[0]['price']
    average_price = (
                        sample_products_package[0]['price'] +
                        sample_products_package[1]['price'] +
                        sample_products_package[2]['price']
                        ) / 3
    expected_score = 100 * (1 - ((product_price - average_price) / average_price))

    # Act
    calculated_score = IssacsInsightScore._calculate_price_score(product_price, average_price)

    # Assert
    assert calculated_score == pytest.approx(expected_score)


def test_verify_price_score_calculation_with_negative_price():
    # Arrange
    product_price = -100
    average_price = 100

    # Act and Assert
    with pytest.raises(ValueError):
        IssacsInsightScore._calculate_price_score(product_price, average_price)


# _calculate_rating_score()

def test_verify_rating_score_calculation(sample_products_package):
    # Arrange
    product_rating = sample_products_package[0]['rating']
    expected_score = (product_rating / 5) * 100

    # Act
    calculated_score = IssacsInsightScore._calculate_rating_score(product_rating)

    # Assert
    assert calculated_score == pytest.approx(expected_score)


def test_verify_rating_score_calculation_with_null_rating():
    # Arrange
    product_rating = None

    # Act and Assert
    with pytest.raises(TypeError):
        IssacsInsightScore._calculate_rating_score(product_rating)


# _calculate_reviews_score()

def test_verify_reviews_score_calculation(sample_products_package):
    # Arrange
    product_reviews = sample_products_package[0]['reviews']
    max_reviews = sample_products_package[2]['reviews']
    expected_score = (np.log(product_reviews + 1) / np.log(max_reviews + 1)) * 100

    # Act
    calculated_score = IssacsInsightScore._calculate_reviews_score(product_reviews, max_reviews)

    # Assert
    assert calculated_score == pytest.approx(expected_score)


def test_reviews_score_zero_reviews():
    # Arrange
    product_reviews = 0
    max_reviews = 100

    # Act
    score = IssacsInsightScore._calculate_reviews_score(product_reviews, max_reviews)

    # Assert
    assert score == 0


def test_reviews_score_equal_reviews():
    # Arrange
    product_reviews = 100
    max_reviews = 100

    # Act
    score = IssacsInsightScore._calculate_reviews_score(product_reviews, max_reviews)

    # Assert
    assert score == 100


def test_reviews_score_product_greater_than_max():
    # Arrange
    product_reviews = 150
    max_reviews = 100

    # Act & Assert
    with pytest.raises(ValueError):
        IssacsInsightScore._calculate_reviews_score(product_reviews, max_reviews)


# _find_max_product_and_store_reviews()

def test_max_reviews_no_null_reviews():
    # Arrange
    products = [
        {"reviews": 10, "store_reviews": 100},
        {"reviews": 5, "store_reviews": 50},
        {"reviews": 15, "store_reviews": 150},
        {"reviews": 20, "store_reviews": 200},
        {"reviews": 1, "store_reviews": 10}
    ]
    expected_max_reviews_return = 20
    expected_max_store_reviews_return = 200

    # Act
    max_reviews, store_max_reviews = IssacsInsightScore._find_max_product_and_store_reviews(products)

    # Assert
    assert max_reviews == expected_max_reviews_return
    assert store_max_reviews == expected_max_store_reviews_return

def test_max_reviews_with_some_null_reviews():
    # Arrange
    products = [
        {"reviews": None, "store_reviews": 100},
        {"reviews": 5, "store_reviews": 50},
        {"reviews": None, "store_reviews": None},
        {"reviews": 200, "store_reviews": None},
        {"reviews": 1, "store_reviews": 10}
    ]
    expected_max_reviews_return = 200
    expected_max_store_reviews_return = 100

    # Act
    max_reviews, store_max_reviews = IssacsInsightScore._find_max_product_and_store_reviews(products)

    # Assert
    assert max_reviews == expected_max_reviews_return
    assert store_max_reviews == expected_max_store_reviews_return

def test_max_reviews_with_all_null_reviews():
    # Arrange
    products = [
        {"reviews": None, "store_reviews": None},
        {"reviews": None, "store_reviews": None},
        {"reviews": None, "store_reviews": None},
        {"reviews": None, "store_reviews": None},
        {"reviews": None, "store_reviews": None}
    ]
    expected_max_reviews_return = 0
    expected_max_store_reviews_return = 0

    # Act
    max_reviews, store_max_reviews = IssacsInsightScore._find_max_product_and_store_reviews(products)

    # Assert
    assert max_reviews == expected_max_reviews_return
    assert store_max_reviews == expected_max_store_reviews_return

# _calculate_issacs_insight_score()

def test_empty_payload_raises_error(insight_score, empty_products_package):
    with pytest.raises(ValueError):
        insight_score.calculate_issacs_insight_score(empty_products_package)

def test_valid_payload(insight_score, sample_products_package):
    # Arrange
    expected_product_payload = [
        {
            'position': 1,
            'title': 'Star Wars Lightsaber',
            'link': 'https://www.fake-starwars.com/lightsaber',
            'product_id': 'SW123',
            'source': 'StarWarsShop',
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
        }
    ]

    # Act
    updated_product_payload = insight_score.calculate_issacs_insight_score(sample_products_package)

    # Assert
    assert isinstance(updated_product_payload, list)
    assert 'insight_scores' in updated_product_payload[0]
    assert 'insight_scores' in updated_product_payload[1]
    assert 'insight_scores' in updated_product_payload[2]
    assert 'insight_score_weights' in updated_product_payload[0]
    assert 'insight_score_weights' in updated_product_payload[1]
    assert 'insight_score_weights' in updated_product_payload[2]
    assert 'final_issacs_insight_score' in updated_product_payload[0]
    assert 'final_issacs_insight_score' in updated_product_payload[1]
    assert 'final_issacs_insight_score' in updated_product_payload[2]
    assert updated_product_payload == expected_product_payload

def test_null_values_payload(insight_score, null_values_products_package):
    # Arrange
    expected_product_payload = [
        {
            'title': 'X-Wing Model',
            'price': 100.0,
            'rating': 4.2,
            'reviews': 450,
            'store_rating': 4.5,
            'store_reviews': 1000,
            'insight_scores': {
                'price_score': 133.33,
                'rating_score': 84.0,
                'reviews_score': 96.83,
                'store_rating_score': 90.0,
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
                'final_issacs_insight_score': 102
            }
        }, {
            'title': 'TIE Fighter Toy',
            'price': None,
            'rating': 4.1,
            'reviews': 300,
            'store_rating': 4.4,
            'store_reviews': 900,
            'insight_scores': {
                'price_score': None,
                'rating_score': 82.0,
                'reviews_score': 90.42,
                'store_rating_score': 88.0,
                'store_reviews_score': 98.48
            },
            'insight_score_weights': {
                'price_score_weight': 0,
                'rating_score_weight': 0.39999999999999997,
                'reviews_score_weight': 0.3333333333333333,
                'store_rating_score_weight': 0.13333333333333333,
                'store_reviews_score_weight': 0.13333333333333333,
                'total_weight': 0.75
            },
            'final_issacs_insight_score': {
                'final_issacs_insight_score': 88
            }
        }, {
            'title': 'Rebel Pilot Helmet',
            'price': 200.0,
            'rating': None,
            'reviews': None,
            'store_rating': 4.3,
            'store_reviews': 800,
            'insight_scores': {
                'price_score': 66.67,
                'rating_score': None,
                'reviews_score': None,
                'store_rating_score': 86.0,
                'store_reviews_score': 96.77
            },
            'insight_score_weights': {
                'price_score_weight': 0.5555555555555556,
                'rating_score_weight': 0,
                'reviews_score_weight': 0,
                'store_rating_score_weight': 0.22222222222222227,
                'store_reviews_score_weight': 0.22222222222222227,
                'total_weight': 0.44999999999999996
            },
            'final_issacs_insight_score': {
                'final_issacs_insight_score': 78
            }
        }, {
            'title': 'Stormtrooper Armor',
            'price': None,
            'rating': 3.8,
            'reviews': 550,
            'store_rating': None,
            'store_reviews': None,
            'insight_scores': {
                'price_score': None,
                'rating_score': 76.0,
                'reviews_score': 100.0,
                'store_rating_score': None,
                'store_reviews_score': None
            },
            'insight_score_weights': {
                'price_score_weight': 0,
                'rating_score_weight': 0.5454545454545454,
                'reviews_score_weight': 0.45454545454545453,
                'store_rating_score_weight': 0,
                'store_reviews_score_weight': 0,
                'total_weight': 0.55
            },
            'final_issacs_insight_score': {
                'final_issacs_insight_score': 87
            }
        }, {
            'title': 'Chewbacca Plush',
            'price': None,
            'rating': None,
            'reviews': None,
            'store_rating': 4.2,
            'store_reviews': None,
            'insight_scores': {
                'price_score': None,
                'rating_score': None,
                'reviews_score': None,
                'store_rating_score': 84.0,
                'store_reviews_score': None
            },
            'insight_score_weights': {
                'price_score_weight': 0,
                'rating_score_weight': 0,
                'reviews_score_weight': 0,
                'store_rating_score_weight': 1.0,
                'store_reviews_score_weight': 0,
                'total_weight': 0.1
            },
            'final_issacs_insight_score': {
                'final_issacs_insight_score': 84
            }
        }, {
            'title': 'Death Star Planter',
            'price': None,
            'rating': None,
            'reviews': None,
            'store_rating': None,
            'store_reviews': None,
            'insight_scores': {
                'price_score': None,
                'rating_score': None,
                'reviews_score': None,
                'store_rating_score': None,
                'store_reviews_score': None
            },
            'insight_score_weights': {
                'price_score_weight': 0,
                'rating_score_weight': 0,
                'reviews_score_weight': 0,
                'store_rating_score_weight': 0,
                'store_reviews_score_weight': 0,
                'total_weight': 0.0
            },
            'final_issacs_insight_score': {
                'final_issacs_insight_score': 0
            }
        }
    ]

    # Act
    updated_product_payload = insight_score.calculate_issacs_insight_score(null_values_products_package)

    # Assert
    assert isinstance(updated_product_payload, list)
    assert 'insight_scores' in updated_product_payload[0]
    assert 'insight_scores' in updated_product_payload[1]
    assert 'insight_scores' in updated_product_payload[5]
    assert 'insight_score_weights' in updated_product_payload[1]
    assert 'insight_score_weights' in updated_product_payload[2]
    assert 'insight_score_weights' in updated_product_payload[3]
    assert 'final_issacs_insight_score' in updated_product_payload[0]
    assert 'final_issacs_insight_score' in updated_product_payload[2]
    assert 'final_issacs_insight_score' in updated_product_payload[4]
    assert updated_product_payload == expected_product_payload