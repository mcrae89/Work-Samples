import pytest
import pytz
import random
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')

def connect_to_DB():
    connection = psycopg2.connect(DATABASE_URL)

    cursor = connection.cursor()

    return connection, cursor

def fetch_product_from_DB(name):
    connection, cursor = connect_to_DB()

    try:
        query = """
        SELECT id, identifier, product_name, issacs_insight, last_updated_date
        FROM Products
        WHERE product_name = %s
        LIMIT 1; 
        """

        cursor.execute(query, (name,))
        
        row = cursor.fetchone()

        if row is None:
            return None

        denver_tz = pytz.timezone('America/Denver')
        product['last_updated_date'] = product['last_updated_date'].replace(tzinfo=pytz.utc).astimezone(denver_tz)
        column_names = [desc[0] for desc in cursor.description]
        product = dict(zip(column_names, row))

        return product

    except Exception as e:
        print(f"Error fetching product data: {e}")
        return None

    finally:
        cursor.close()
        connection.close()

def fetch_prices_from_DB(id):
    connection, cursor = connect_to_DB()

    try:
        query = """
        SELECT id, price, price_url, retailer
        FROM Prices
        WHERE product_id = %s; 
        """ 

        cursor.execute(query, (id,))
        
        rows = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]

        prices_list = [dict(zip(column_names, row)) for row in rows]
        return prices_list

    except Exception as e:
        print(f"Error fetching price data: {e}")
        return None

    finally:
        cursor.close()
        connection.close()

def fetch_reviews_from_DB(id):
    connection, cursor = connect_to_DB()

    try:
        query = """
        SELECT user_name, review, review_date
        FROM Reviews
        WHERE product_id = %s; 
        """ 

        cursor.execute(query, (id,))
        
        rows = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]

        reviews_list = [dict(zip(column_names, row)) for row in rows]
        return reviews_list

    except Exception as e:
        print(f"Error fetching review data: {e}")
        return None

    finally:
        cursor.close()
        connection.close()

def fetch_best_price_from_DB(id):
    connection, cursor = connect_to_DB()

    try:
        query = """
        SELECT price, price_url 
        FROM Prices
        WHERE product_id = %s 
        ORDER BY Prices.price ASC 
        LIMIT 1;
        """
        
        cursor.execute(query, (id,))
        bestPrice = cursor.fetchone()

        if bestPrice is None:
            return None

        column_names = [desc[0] for desc in cursor.description]
        best_price_dict = dict(zip(column_names, bestPrice))

        return best_price_dict

    except Exception as e:
        print(f"Error fetching best price: {e}")
        return None

    finally:
        cursor.close()
        connection.close()

def test_homepage():
    # Send an HTTP GET request to the homepage
    url = 'https://issacs-index-c54596d5a666.herokuapp.com/'
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    assert response.status_code == 200, f"Failed to access the homepage. Status code: {response.status_code}"

    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.text, 'html.parser')

    # Check if the title contains "Issac's Index Download"
    title_tag = soup.find('title')
    assert title_tag is not None, "Title not found in the HTML"
    assert "Issac's Index Download" in title_tag.get_text(), "Title does not contain 'Issac's Index Download'"

    # Check if the "Download Extension" button exists
    download_button = soup.find('button', class_='btn btn-primary')
    assert download_button is not None, "Download Extension button not found"

# Define a fixture to get random products
@pytest.fixture
def random_products():
    connection, cursor = connect_to_DB()
    try:
        query = "SELECT product_name FROM Products"
        cursor.execute(query)
        products = [row[0] for row in cursor.fetchall()]
        return products if len(products) < 10 else random.sample(products, 10)
    finally:
        cursor.close()
        connection.close()


def test_product_page(random_products):
    products = random_products
    for name in products:
        # Send an HTTP GET request to the web page
        url = f"https://issacs-index-c54596d5a666.herokuapp.com/product/{name}"
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        assert response.status_code == 200, f"Failed to access the product page for name {name}. Status code: {response.status_code}"

        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, 'html.parser')

        # Fetch product data from the database
        product = fetch_product_from_DB(name)
        if product is None:
            print(f"Product {name} not found in the database, skipping...")
            continue

        # Validate product name is displayed
        product_name_element = soup.find(id="ProductName")
        assert product_name_element is not None, "Product name element not found in the HTML"
        product_name = product_name_element.text.strip()
        assert product_name == product["product_name"], f"Product name mismatch for name {name}"

        # Validate last updated date
        date_element = soup.find(id="updatedDate")
        assert date_element is not None, "Last updated date element not found in the HTML"
        actual_date_str = date_element.text.replace("Updated - ", "").strip()
        denver_tz = pytz.timezone('America/Denver')
        actual_date = datetime.strptime(actual_date_str, "%m/%d/%Y %I:%M %p")
        actual_date = denver_tz.localize(actual_date)
        expected_date = product["last_updated_date"].replace(tzinfo=pytz.utc).astimezone(denver_tz)
        assert actual_date_str == expected_date, f"Last updated date mismatch for name {name}"

        # Test the "Best Price" link
        best_price_data = fetch_best_price_from_DB(product["id"])
        best_price_link_element = soup.find(id="bestPrice")
        assert best_price_link_element is not None, "Best Price link element not found in the HTML"
        best_price_link = best_price_link_element.get("href")
        assert best_price_link == best_price_data["price_url"], f"Best Price link mismatch for name {name}"

        # Test all retailer price links in the price list
        prices = fetch_prices_from_DB(product["id"])
        price_links = soup.select("div.scroll-content-prices a")
        for link in price_links:
            link_id = link.get("id")
            link_url = link.get("href")

            # Find the matching price entry using list comprehension
            matching_price = next((price for price in prices if price["id"] == int(link_id)), None)
            
            if matching_price is not None:
                db_link_url = matching_price["price_url"]
                assert link_url == db_link_url, f"URL mismatch for link with ID {link_id}: Expected '{db_link_url}', but found '{link_url}'"
            else:
                assert False, f"No matching database entry for link with ID {link_id}"

        # Extract prices from fetched data
        db_prices = [item for item in prices if item.get("price")]

        # Fetch displayed prices from the webpage
        prices_elements = soup.select("#prices .record-price")
        displayed_prices = []
        for price_element in prices_elements:
            retailer_name = price_element.select_one(".name-cell").text
            price_text = price_element.select_one(".price-cell").text

            # Remove dollar sign and convert to float for easy comparison
            price_value = float(price_text.replace("$", ""))

            displayed_price = {
                "retailer": retailer_name,
                "price": price_value
            }
            displayed_prices.append(displayed_price)

        # Compare displayed prices with the ones in the database
        for db_price in db_prices:
            expected_price = {
                "retailer": db_price["retailer"],
                "price": float(db_price["price"])
            }
            assert expected_price in displayed_prices, f"Expected {expected_price} not found in displayed prices for name {name}"

        # Fetch reviews from the database
        db_reviews = fetch_reviews_from_DB(product["id"])

        # Fetch displayed reviews from the webpage
        reviews_elements = soup.select("#reviews .record-review")
        displayed_reviews = []
        for review_element in reviews_elements:
            user_name = review_element.select_one(".username-cell").text.strip()
            review_text = review_element.select_one(".review-cell").text.strip()
            review_date = review_element.select_one(".date-cell").text.strip()

            displayed_review = {
                "user_name": user_name,
                "review": review_text,
                "review_date": review_date
            }
            displayed_reviews.append(displayed_review)

        # Compare displayed reviews with the ones in the database
        for db_review in db_reviews:
            db_review['review_date'] = db_review['review_date'].date()
            db_review_date_str = db_review["review_date"].strftime("%m/%d/%Y")  # Format as dd/mm/yyyy
            displayed_review_match = {
                "user_name": db_review["user_name"].strip(),
                "review": db_review["review"].strip(),
                "review_date": db_review_date_str
            }
            # Assert that the review from the database is in the displayed reviews
            assert displayed_review_match in displayed_reviews, f"Review not found in displayed reviews for user_name {db_review['user_name']}"

        # Ensure all displayed reviews are also in the database
        for displayed_review in displayed_reviews:
            displayed_review_date_str = displayed_review["review_date"]
            # Parse the string to a datetime object
            displayed_review_date = datetime.strptime(displayed_review_date_str, "%m/%d/%Y").date()
            db_review_match = {
                "user_name": displayed_review["user_name"].strip(),
                "review": displayed_review["review"].strip(),
                "review_date": displayed_review_date
            }
            # Assert that the displayed review is in the database reviews
            assert db_review_match in db_reviews, f"Displayed review not found in the database for user_name {displayed_review['user_name']}"

if __name__ == "__main__":
    pytest.main([__file__])
