// service_worker.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "fetchData") {
        fetchScrapeData(message.url)
            .then(data => {
                handleData(data);
                // Additional actions can be taken here if needed
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }
});

function fetchScrapeData(url) {
    const apiUrl = new URL('https://issacs-index-c54596d5a666.herokuapp.com/scrape');
    apiUrl.searchParams.append('url', url);

    return fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();  // Read the response stream once and return
        })
        .then(data => {
            data.source_url = url;  // Add the source URL to the data
            return data;  // Pass the data forward
        });
}

// After saving data and posting prices data, trigger the product data processing
function handleData(data) {
    postDataToAPI(data)
        .then(productData => {
           // console.log('Product Data Success:', productData);
            return postPricesDataToAPI(extractPricesData(data));
        })
        .then(pricesData => {
           // console.log('Prices Data Success:', pricesData);
            return triggerProductData(data);
        })
        .then(triggeredProductData => {
            //console.log('Triggered Product Data:', triggeredProductData);
        
            if (triggeredProductData) {
                // Store the data in chrome.storage.local
                chrome.storage.local.set({ 'triggeredProductData': triggeredProductData }, () => {
        
                    // Create a notification
                    chrome.notifications.create({
                        type: 'basic',
                        iconUrl: 'images/issacLoading.png', // Path to your extension's icon
                        title: "Issac's Index",
                        message: 'Additional prices have been found!',
                        priority: 2
                    });
                });
            }
        })
        .catch(error => {
            console.error('Error in processing data:', error);
        });
}

function postDataToAPI(data) {
    return fetch('https://issacs-index-c54596d5a666.herokuapp.com/products/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            products: [{
                product_name: data.productName,
                identifier: data.upc,
                source_url: data.source_url.split('?')[0],
                retailer: data.retailer.replace('.com', '')
            }]
        }),
    })
    .then(response => response.json())
    .then(productData => {
        //console.log('Product Data Success:', productData);
        return productData; // Return the response for further processing
    })
    .catch((error) => {
        console.error('Error:', error);
        throw error; // Re-throw the error for handling in subsequent chains
    });
}

function extractPricesData(data) {
    return {
        prices: [{
            product_name: data.productName,
            price: parseFloat(data.price.replace(/[^\d.-]/g, '')), // converting the price string to a number
            retailer: data.retailer.replace('.com', ''),
            price_url: data.source_url.split('?')[0]
        }],
        product_name: data.productName
    };
}

function postPricesDataToAPI(pricesData) {
    let apiUrl = 'https://issacs-index-c54596d5a666.herokuapp.com/prices/';
    fetch( apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(pricesData),
    })
    .then(response => response.json())
    .then(data => {
       // console.log('Prices Data Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function triggerProductData(savedData) {
    return fetch('https://issacs-index-c54596d5a666.herokuapp.com/ce/trigger-product-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_name: savedData.productName,
            price: parseFloat(savedData.price.replace(/[^\d.-]/g, '')), // converting the price string to a number
            retailer_name: savedData.retailer.replace('.com', ''),
            uri: savedData.source_url.split('?')[0]
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        console.log(response);
        return response.text();
    })
    .then(responseText => {
        const triggeredProductData = JSON.parse(responseText);
        return triggeredProductData;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Object to keep track of tab URLs
let tabUrls = {};

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    // Check if the tab was previously tracked and if its URL has changed
    const isReload = tabUrls[tabId] && tabUrls[tabId] === tab.url;

    // Update the stored URL for the tab
    tabUrls[tabId] = tab.url;

    if (changeInfo.status === 'loading' && tab.active && isReload) {
        // Clear storage if the active tab is reloaded
        chrome.storage.local.remove('triggeredProductData');
    }
});

// Listen for when a tab is closed and remove it from the tracking object
chrome.tabs.onRemoved.addListener((tabId) => {
    delete tabUrls[tabId];
});

// module.exports = {
//     fetchScrapeData,
//     handleData,
//     postDataToAPI,
//     extractPricesData,
//     postPricesDataToAPI,
//     triggerProductData
// };