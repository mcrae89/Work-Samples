import numpy as np

class IssacsInsightScore:
    @staticmethod
    def _find_average_price(products_package):
        """
        Calculates the average price of the products in the payload, ignoring None values.
        :param products_package: List of product dictionaries
        :return: Average price of all products - float
        """
        total_price = 0
        count = 0
        for product in products_package:
            price = product.get('price')
            if price is not None:
                total_price += price
                count += 1

        average_price = total_price / count
        return average_price

    @staticmethod
    def _find_max_product_and_store_reviews(products_payload):
        """
        Calculates the maximum number of reviews for product reviews and store reviews in the payload.
        :param products_payload: List of product dictionaries
        :return: Tuple of maximum product reviews and maximum store reviews - integers
        """
        reviews_list = []
        store_reviews_list = []
        for product in products_payload:
            if product.get('reviews') is not None:
                reviews_list.append(product['reviews'])
            if product.get('store_reviews') is not None:
                store_reviews_list.append(product['store_reviews'])

        max_reviews = max(reviews_list) if len(reviews_list) > 0 else 0
        max_store_reviews = max(store_reviews_list) if len(store_reviews_list) > 0 else 0
        return max_reviews, max_store_reviews

    @staticmethod
    def _calculate_price_score(product_price, average_price):
        """
        Calculates the price score for a product based on how its price compares to the average price of all products.
        :param product_price: Price of the product
        :param average_price: Average price of all products
        :return: Price score - float
        """
        if product_price <= 0 or average_price <= 0:
            raise ValueError("Product price or Average Price cannot be zero or negative")
        price_difference = product_price - average_price
        price_score = 100 * (1 - (price_difference / average_price))
        return price_score

    @staticmethod
    def _calculate_rating_score(product_rating):
        """
        Calculates the rating score for a product, scaling the rating to a 0-100 range
        :param product_rating: Rating of the product
        :return: Rating score - float
        """
        rating_score = product_rating * 20
        return rating_score

    @staticmethod
    def _calculate_reviews_score(product_reviews, max_reviews):
        """
        Calculates the product reviews score for a product using a logarithmic scale,
        normalizing the maximum number of reviews.
        :param product_reviews: Number of reviews for the product
        :param max_reviews: Maximum number of reviews among all products
        :return: Reviews score - float
        """
        if product_reviews > max_reviews:
            raise ValueError("Product reviews cannot be greater than maximum reviews")
        reviews_log = np.log(product_reviews + 1)
        max_reviews_log = np.log(max_reviews + 1)
        reviews_score = (reviews_log / max_reviews_log) * 100
        return reviews_score

    def calculate_issacs_insight_score(self, products_payload):
        """
        Calculates individual product scores in the products_payload, including Isaac's Insight score,
        with dynamic weight adjustments based on the presence of None values.
        Appends individual scores, weights, and Insight score to each product in the payload.
        :param products_payload: List of product dictionaries
        :return: The same products_payload list with appended scores, weights, and Insight score
        """
        if len(products_payload) == 0:
            raise ValueError("Products payload cannot be empty")

        average_price = self._find_average_price(products_payload)
        max_reviews, max_store_reviews = self._find_max_product_and_store_reviews(products_payload)

        insight_score_weights = {
            'price_score_weight': 0.25,
            'rating_score_weight': 0.3,
            'reviews_score_weight': 0.25,
            'store_rating_score_weight': 0.1,
            'store_reviews_score_weight': 0.1
        }
        # Calculate individual scores
        for product in products_payload:
            # Extract product data
            product_price = product.get('price')
            product_rating = product.get('rating')
            product_reviews = product.get('reviews')
            product_store_rating = product.get('store_rating')
            product_store_reviews = product.get('store_reviews')

            # Calculate scores
            if product_price is not None:
                price_score = round(self._calculate_price_score(product_price, average_price), 2)
            else:
                price_score = None
            if product_rating is not None:
                rating_score = round(self._calculate_rating_score(product_rating), 2)
            else:
                rating_score = None
            if product_reviews is not None:
                reviews_score = round(self._calculate_reviews_score(product_reviews, max_reviews), 2)
            else:
                reviews_score = None
            if product_store_rating is not None:
                store_rating_score = round(self._calculate_rating_score(product_store_rating), 2)
            else:
                store_rating_score = None
            if product_store_reviews is not None:
                store_reviews_score = round(self._calculate_reviews_score(product_store_reviews, max_store_reviews), 2)
            else:
                store_reviews_score = None

            # Individual scores dictionary for products payload
            insight_scores = {
                'price_score': price_score,
                'rating_score': rating_score,
                'reviews_score': reviews_score,
                'store_rating_score': store_rating_score,
                'store_reviews_score': store_reviews_score
            }
            # Base score weights dictionary for products payload
            insight_score_weights = {
                'price_score_weight': 0.25,
                'rating_score_weight': 0.3,
                'reviews_score_weight': 0.25,
                'store_rating_score_weight': 0.1,
                'store_reviews_score_weight': 0.1,
                'total_weight': 1.0
            }

            # Check for None score values. If none, update total_weight score weights based on None values
            if price_score is None:
                updated_total_weight = insight_score_weights['total_weight'] - insight_score_weights['price_score_weight']
                insight_score_weights['total_weight'] = updated_total_weight
                insight_score_weights['price_score_weight'] = 0
            if rating_score is None:
                updated_total_weight = insight_score_weights['total_weight'] - insight_score_weights['rating_score_weight']
                insight_score_weights['total_weight'] = updated_total_weight
                insight_score_weights['rating_score_weight'] = 0
            if reviews_score is None:
                updated_total_weight = insight_score_weights['total_weight'] - insight_score_weights['reviews_score_weight']
                insight_score_weights['total_weight'] = updated_total_weight
                insight_score_weights['reviews_score_weight'] = 0
            if store_rating_score is None:
                updated_total_weight = insight_score_weights['total_weight'] - insight_score_weights['store_rating_score_weight']
                insight_score_weights['total_weight'] = updated_total_weight
                insight_score_weights['store_rating_score_weight'] = 0
            if store_reviews_score is None:
                updated_total_weight = insight_score_weights['total_weight'] - insight_score_weights['store_reviews_score_weight']
                insight_score_weights['total_weight'] = updated_total_weight
                insight_score_weights['store_reviews_score_weight'] = 0

            # Dynamically adjusts each weight based on None values
            if insight_score_weights['total_weight'] != 1.0:
                for key, weight in insight_score_weights.items():
                    if key != 'total_weight' and weight != 0:
                        updated_weight = weight / insight_score_weights['total_weight']
                        insight_score_weights[key] = updated_weight

            # Calculate final Isaac's Insight Score
            issacs_insight_score = 0
            issacs_insight_score += price_score * insight_score_weights['price_score_weight'] if price_score is not None else 0
            issacs_insight_score += rating_score * insight_score_weights['rating_score_weight'] if rating_score is not None else 0
            issacs_insight_score += reviews_score * insight_score_weights['reviews_score_weight'] if reviews_score is not None else 0
            issacs_insight_score += store_rating_score * insight_score_weights['store_rating_score_weight'] if store_rating_score is not None else 0
            issacs_insight_score += store_reviews_score * insight_score_weights['store_reviews_score_weight'] if store_reviews_score is not None else 0
            issacs_insight_score = int(round(issacs_insight_score, 0))
            final_issacs_insight_score = {"final_issacs_insight_score": issacs_insight_score}

            # Update product payload with insight_scores, insight_score_weights, and final_insight_score
            product['insight_scores'] = insight_scores
            product['insight_score_weights'] = insight_score_weights
            product['final_issacs_insight_score'] = final_issacs_insight_score

        return products_payload