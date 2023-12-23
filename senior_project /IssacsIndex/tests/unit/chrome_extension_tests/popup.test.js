// popup.test.js
global.TextEncoder = require('util').TextEncoder;
global.TextDecoder = require('util').TextDecoder;
const { JSDOM } = require('jsdom');
const { updateProducts, updateReviews, updateWebsiteLink } = require('../../../chrome_extension/popup.js');

describe('popup.js tests', () => {
    let document;
    let chrome;

    beforeEach(() => {
        // Set up a mock DOM
        const dom = new JSDOM('<!doctype html><html><body></body></html>');
        global.window = dom.window;
        document = global.window.document;

        // Set up a mock chrome API
        chrome = {
            tabs: {
                create: jest.fn()
            }
        };
        global.chrome = chrome;
    });

    test('updateProducts updates the prices div correctly', () => {
        const pricesDiv = document.createElement('div');
        pricesDiv.id = 'prices';
        document.body.appendChild(pricesDiv);

        const products = [
            { link: 'link1', thumbnail: 'thumbnail1', source: 'source1', title: 'title1', price: '1.23' },
            { link: 'link2', thumbnail: 'thumbnail2', source: 'source2', title: 'title2', price: '4.56' }
        ];

        updateProducts(products);

        expect(pricesDiv.innerHTML).toContain('link1');
        expect(pricesDiv.innerHTML).toContain('thumbnail1');
        expect(pricesDiv.innerHTML).toContain('source1');
        expect(pricesDiv.innerHTML).toContain('title1');
        expect(pricesDiv.innerHTML).toContain('$1.23');
        expect(pricesDiv.innerHTML).toContain('link2');
        expect(pricesDiv.innerHTML).toContain('thumbnail2');
        expect(pricesDiv.innerHTML).toContain('source2');
        expect(pricesDiv.innerHTML).toContain('title2');
        expect(pricesDiv.innerHTML).toContain('$4.56');
    });

    test('updateReviews updates the reviews div correctly', () => {
        const reviewsDiv = document.createElement('div');
        reviewsDiv.id = 'reviews';
        document.body.appendChild(reviewsDiv);

        const reviews = [
            { source: 'source1', review_date: 'date1', product_name: 'name1', title: 'title1', review: 'review1' },
            { source: 'source2', review_date: 'date2', product_name: 'name2', title: 'title2', review: 'review2' }
        ];

        updateReviews(reviews);

        expect(reviewsDiv.innerHTML).toContain('source1');
        expect(reviewsDiv.innerHTML).toContain('date1');
        expect(reviewsDiv.innerHTML).toContain('name1');
        expect(reviewsDiv.innerHTML).toContain('title1');
        expect(reviewsDiv.innerHTML).toContain('review1');
        expect(reviewsDiv.innerHTML).toContain('source2');
        expect(reviewsDiv.innerHTML).toContain('date2');
        expect(reviewsDiv.innerHTML).toContain('name2');
        expect(reviewsDiv.innerHTML).toContain('title2');
        expect(reviewsDiv.innerHTML).toContain('review2');
    });

    test('updateWebsiteLink updates the website link correctly', () => {
        const websiteLink = document.createElement('a');
        websiteLink.id = 'websiteLink';
        document.body.appendChild(websiteLink);

        const triggeredProduct = { product_name: 'name1' };

        updateWebsiteLink(triggeredProduct);

        expect(websiteLink.href).toBe('https://issacs-index-c54596d5a666.herokuapp.com/product/name1');
        expect(chrome.tabs.create).not.toHaveBeenCalled();

        // Simulate a click event
        const clickEvent = new window.MouseEvent('click', {
            view: window,
            bubbles: true,
            cancelable: true
        });
        websiteLink.dispatchEvent(clickEvent);

        expect(chrome.tabs.create).toHaveBeenCalledWith({ url: 'https://issacs-index-c54596d5a666.herokuapp.com/product/name1' });
    });
});