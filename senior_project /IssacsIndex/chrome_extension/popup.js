// popup.js
document.addEventListener('DOMContentLoaded', () => {
    chrome.storage.local.get('triggeredProductData', (result) => {
        if (result.triggeredProductData) {
            // Hide the loading content
            document.getElementById('loadingContent').style.display = 'none';

            // Show and populate the product details
            const productDetailsDiv = document.getElementById('productDetails');
            productDetailsDiv.style.display = 'block';
            updateProducts(result.triggeredProductData[0].products);
            updateReviews(result.triggeredProductData[1].reviews);
            updateWebsiteLink(result.triggeredProductData[0].triggered_product_position);
        }
    });
});

function updateProducts(products) {
    const pricesDiv = document.getElementById('prices');
    let htmlContent = '';

    if (products && products.length > 0) {
        // Sort products by price in ascending order
        products.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));

        products.forEach(product => {
            htmlContent += `<a href="${product.link}" target="_blank" style="text-decoration: none; color: inherit;">
                                <div class="record-price">
                                    <div class="logo-cell">
                                        <img src="${product.thumbnail}" style="width: 3em; height: 3em;">
                                    </div>
                                    <span class="name-cell">${product.source}</span>
                                    <span class="product-cell">${product.title}</span>
                                    <span class="price-cell" id="priceCell">$${parseFloat(product.price).toFixed(2)}</span>
                                </div>
                            </a>`;
        });
    } else {
        htmlContent = '<p> No prices found for this product. </p>';
    }

    pricesDiv.innerHTML = htmlContent;
}

function updateReviews(reviews) {
    const reviewsDiv = document.getElementById('reviews');
    let htmlContent = '';

    if (reviews && reviews.length > 0) {
        reviews.forEach(review => {
            htmlContent += `<div class="record-review">
                                <div class="review-row">
                                    <span class="source-cell"> ${review.source} </span>
                                    <span class="date-cell"> 
                                        ${review.review_date}
                                    </span>
                                </div>
                                <div class="row">
                                    <span class="review-product-cell"> <strong>${review.product_name } </strong> </span> 
                                </div>
                                <div class="row">
                                    <span class="review-title"> ${review.title } </span>
                                </div>
                                <div class="row">
                                    <span class="review-cell"> ${review.review } </span>                                                                                                          
                                </div>
                            </div>`;
        });
    } else {
        htmlContent = '<p> No reviews found for this product. </p>';
    }

    reviewsDiv.innerHTML = htmlContent;
}

function updateWebsiteLink(triggeredProduct) {
    const websiteLink = document.getElementById('websiteLink');
    if (triggeredProduct) {
        const productUrl = `https://issacs-index-c54596d5a666.herokuapp.com/product/${encodeURIComponent(triggeredProduct.product_name)}`;
        websiteLink.href = productUrl;
        
        // Add event listener to open the link in a new tab
        websiteLink.addEventListener('click', (event) => {
            event.preventDefault(); // Prevent default anchor tag behavior
            chrome.tabs.create({ url: productUrl });
        });
    }
}

// module.exports = { updateProducts, updateReviews, updateWebsiteLink };