--\c IssacsIndex

DO $$
DECLARE
    product_id INT := 1;
    identifier_code BIGINT := 123456789012; -- Starting identifier code for illustration
    product_name_prefix TEXT := 'Product ';
    product_description TEXT := 'This is a sample product description';
    issacs_insight_val INT := 50;
    source_url_base TEXT := 'http://127.0.0.1:5000/product/';
BEGIN
    WHILE product_id <= 50 LOOP
        INSERT INTO Products (identifier, product_name, product_description, issacs_insight, source_url) 
        VALUES (
            LPAD(identifier_code::TEXT, 12, '0'), -- Ensure identifier code has 12 digits
            product_name_prefix || product_id,
            product_description || ' for product ' || product_id,
            issacs_insight_val,
            source_url_base || product_id
        );

        -- Increment values for next iteration
        product_id := product_id + 1;
        identifier_code := identifier_code + 1;
        issacs_insight_val := issacs_insight_val + 10; -- Arbitrary increment for example
    END LOOP;
END $$;

DO $$ 
DECLARE 
   product_counter INT := 1;
   price_counter INT;
   current_price DECIMAL(10,2) := 100.99;
   current_retailer TEXT;
   current_url TEXT;

BEGIN
   WHILE product_counter <= 50 LOOP
      price_counter := 1;
      WHILE price_counter <= 50 LOOP
         
         IF MOD(price_counter,2) = 0 THEN
            current_retailer := 'Walmart';
            current_url := 'http://walmart.com/product' || product_counter || '-price' || price_counter;
         ELSE
            current_retailer := 'Best Buy';
            current_url := 'http://bestbuy.com/product' || product_counter || '-price' || price_counter;
         END IF;

         INSERT INTO Prices (product_id, price, price_url, retailer) 
         VALUES (product_counter, current_price, current_url, current_retailer);

         current_price := current_price + 0.5; -- Increase price by 50 cents as an example
         price_counter := price_counter + 1;
      END LOOP;

      product_counter := product_counter + 1;
      current_price := 100.99; -- Resetting to the starting price for the next product
   END LOOP;
END $$;

DO $$
DECLARE
    product_counter INT;
    rating_counter INT;
    random_rating DECIMAL(2,1);
    random_number_of_ratings INT;
BEGIN
    FOR product_counter IN 1..50 LOOP
        FOR rating_counter IN 1..50 LOOP
            -- Generating a random rating between 1.0 and 5.0
            random_rating := 1.0 + TRUNC(5 * RANDOM())::INT * 0.1;
            
            -- Generating a random number of ratings between 1 and 100
            random_number_of_ratings := 1 + TRUNC(100 * RANDOM())::INT;

            -- Inserting the values
            INSERT INTO Ratings (product_id, avg_rating, number_of_ratings) 
            VALUES (product_counter, random_rating, random_number_of_ratings);
        END LOOP;
    END LOOP;
END $$;


DO $$
DECLARE
    product_counter INT;
    review_counter INT;
    random_user_name VARCHAR(255);
    random_review TEXT;
    random_review_date TIMESTAMP;
BEGIN
    FOR product_counter IN 1..50 LOOP
        FOR review_counter IN 1..50 LOOP
            -- Generating random user name
            random_user_name := 'User' || TRUNC(10000 * RANDOM())::INT;

            -- Generating a random review
            random_review := 'This is a sample review for product ' || product_counter || ' by ' || random_user_name;

            -- Generating a random review date within the last year
            random_review_date := NOW() - INTERVAL '1 year' * RANDOM();

            -- Inserting the values
            INSERT INTO Reviews (product_id, user_name, review, review_date) 
            VALUES (product_counter, random_user_name, random_review, random_review_date);
        END LOOP;
    END LOOP;
END $$;
