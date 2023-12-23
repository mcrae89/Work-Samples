from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, select, case
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

db = SQLAlchemy()

# Database functions
def get_all_products():
    current_time=datetime.utcnow()
    time_24_hours_ago = current_time - timedelta(days=1)
    return Product.query.filter(Product.last_updated_date >= time_24_hours_ago).all()

def get_product_by_name(product_name):
    return Product.query.filter_by(product_name=product_name).first()

def add_product(identifier, product_name, product_description, keywords, issacs_insight, source_url, img):
    new_product = Product(identifier=identifier, product_name=product_name, product_description=product_description, keywords=keywords, issacs_insight=issacs_insight, source_url=source_url, img=img, last_updated_date=datetime.utcnow())    
    db.session.add(new_product)
    db.session.commit()
    return new_product

def update_product_by_name(product_name, product_description, keywords, issacs_insight, source_url, img):
    product = get_product_by_name(product_name)
    if not product:
        return None
    product.product_name = product_name
    product.product_description = product_description
    product.keywords = keywords
    product.issacs_insight = issacs_insight
    product.source_url = source_url
    product.img = img
    product.last_updated_date = datetime.utcnow()
    db.session.commit()
    return product

# def get_reviews_by_product_name(product_name):
#     product = get_product_by_name(product_name)
#     return Review.query.filter_by(product_id=product.id).all()

def get_reviews_by_similar_product_name(product_name):
    # Get the product name for the given product_id
    product = get_product_by_name(product_name)
    if not product:
        return []  # or handle the error as you prefer

    # Modify the query to select specific columns
    query = Review.query.join(Product, Review.product_id == Product.id).with_entities(
        Review, Product.product_name
    )

    # Filter based on trigram similarity with the product name obtained from product_id
    query = query.filter(func.similarity(Product.product_name, product_name) > 0.6)
    
    # Execute the query
    result = query.all()

    # Ensure correct unpacking of the result
    formatted_reviews = [{'review': review.serialize, 'product_name': name} for review, name in result]
    
    return formatted_reviews

def add_reviews_by_product_name(reviews_data):
    new_reviews = []
    for data in reviews_data:
        product_name = data.get('product_name')
        product = get_product_by_name(product_name)
        if not product:
            continue

        new_review = Review(
            product_id=product.id,
            source=data['source'],
            title = data['title'],
            review=data['review'],
            review_date=data['review_date'],
            last_updated_date=datetime.utcnow()
        )
        db.session.add(new_review)
        new_reviews.append(new_review)
    db.session.commit()
    return new_reviews


# def get_prices_by_product_name(product_name):
#     product = get_product_by_name(product_name)
#     return Price.query.filter_by(product_id=product.id).all()

def get_prices_by_similar_product_name(product_name):
    # Get the product name for the given product_id
    product = get_product_by_name(product_name)
    if not product:
        return []  # or handle the error as you prefer

    # Get the current time and subtract 24 hours to define the time frame
    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)

    # Modify the query to select specific columns and filter based on the last update date
    query = Price.query.join(Product, Price.product_id == Product.id).with_entities(
        Price, Product.product_name, Product.img  # Include the img column
    ).filter(
        Price.last_updated_date >= twenty_four_hours_ago,  # Filter for prices updated in the last 24 hours
        func.similarity(Product.product_name, product_name) > 0.6  # Existing similarity filter
    )

    # Order the results first by matching product name, then by product name alphabetically, and finally by price
    query = query.order_by(Price.price.asc())

    # Execute the query
    result = query.all()

    # Ensure correct unpacking of the result
    formatted_prices = [{'price': price.serialize, 'product_name': name, 'image_url': img} for price, name, img in result]

    return formatted_prices


def add_prices_by_product_name(prices_data):
    new_prices = []
    for data in prices_data:
        product_name = data.get('product_name')
        product = get_product_by_name(product_name)
        if not product:
            # If product is not found, skip this entry and continue with the next
            continue

        try:
            new_price = Price(
                product_id=product.id,
                price=data['price'],
                price_url=data['price_url'],
                retailer=data['retailer'],
                last_updated_date=datetime.utcnow()
            )
            db.session.add(new_price)
            new_prices.append(new_price)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            # Handle the unique constraint violation, e.g., update existing record or skip
            existing_price = Price.query.filter_by(price_url=data['price_url']).first()
            if existing_price:
                existing_price.price = data['price']
                existing_price.last_updated_date = datetime.utcnow()
                db.session.commit()

    return new_prices

# def get_ratings_by_product_name(product_name):
#     product = get_product_by_name(product_name)
#     return Rating.query.filter_by(product_id=product.id).all()

def get_ratings_by_similar_product_name(product_name):
    # Get the product name for the given product_id
    product = get_product_by_name(product_name)
    if not product:
        return []  # or handle the error as you prefer

    # Modify the query to select specific columns
    query = Rating.query.join(Product, Rating.product_id == Product.id).with_entities(
        Rating, Product.product_name
    )

    # Filter based on trigram similarity with the product name obtained from product_id
    query = query.filter(func.similarity(Product.product_name, product_name) > 0.6)
    
    # Execute the query
    result = query.all()

    # Ensure correct unpacking of the result
    formatted_ratings = [{'rating': rating.serialize, 'product_name': name} for rating, name in result]
    
    return formatted_ratings

def add_ratings_by_product_name(ratings_data):
    new_ratings = []
    for data in ratings_data:
        product_name = data.get('product_name')
        product = get_product_by_name(product_name)
        if not product:
            continue

        new_rating = Rating(
            product_id=product.id,
            avg_rating=data['avg_rating'],
            number_of_ratings=data['number_of_ratings'],
            last_updated_date=datetime.utcnow()
        )
        db.session.add(new_rating)
        new_ratings.append(new_rating)
    db.session.commit()
    return new_ratings

# Database models
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String, unique=True)
    product_name = db.Column(db.String)
    product_description = db.Column(db.Text)
    keywords = db.Column(db.Text)
    issacs_insight = db.Column(db.Integer)
    source_url = db.Column(db.Text)
    img = db.Column(db.Text)
    last_updated_date = db.Column(db.DateTime)

    # Relationships
    prices = db.relationship('Price', backref='product', lazy='dynamic')
    ratings = db.relationship('Rating', backref='product', lazy='dynamic')
    reviews = db.relationship('Review', backref='product', lazy='dynamic')

class Price(db.Model):
    __tablename__ = 'prices'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    price = db.Column(db.Float)
    price_url = db.Column(db.Text)
    retailer = db.Column(db.String)
    last_updated_date = db.Column(db.DateTime)

class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    avg_rating = db.Column(db.Float)
    number_of_ratings = db.Column(db.Integer)
    last_updated_date = db.Column(db.DateTime)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    source = db.Column(db.String)
    title = db.Column(db.Text)
    review = db.Column(db.Text)
    review_date = db.Column(db.DateTime)
    last_updated_date = db.Column(db.DateTime)

# Extend the models to serialize data
for model in [Product, Price, Rating, Review]:
    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        serialized_data = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                serialized_data[column.name] = value.isoformat()  # Convert datetime to string
            else:
                serialized_data[column.name] = value
        return serialized_data
    model.serialize = serialize