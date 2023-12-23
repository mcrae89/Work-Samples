// product-scraper-v2.test.js
const { setImmediate } = require('timers');
global.setImmediate = setImmediate;
const { describe } = require('node:test');
const { ProductScraper } = require('../../../chrome_extension/product-scraper-v2.js');

describe('Bypass Captcha Tests', () => {
    var scraper = null;
    var testUrl = null;
    beforeAll(() => {
        testUrl = 'https://www.walmart.com/ip/Cosco-6-Foot-Folding-Table-In-White-Speckle/46368979';
        scraper = new ProductScraper(testUrl);
    });
    afterAll(async () => {
        // Close the browser after all tests
        await scraper.closeBrowser();
    });

    test('launches a chromium browser with the stealth plugin', async () => {
        await scraper.initializeBrowser();
        expect(scraper.browser).toBeDefined();
        expect(scraper.browser._options.args).toContain('--disable-blink-features=AutomationControlled');
    });
    
    test('navigates to the url without error', async () => {
        await expect(async () => {
            await scraper.navigatePage();
        }).not.toThrow();
    });

    test('teardown', async () => {
        await scraper.closeBrowser();
        const result = await scraper.navigatePage();
        expect(result).toBeUndefined(); // or whatever value indicates the browser is closed
    });
});

describe('Product Scraper Tests', () => {
    var scraper = null;
    beforeAll(() => {
        const testUrl = 'https://www.walmart.com/ip/Cosco-6-Foot-Folding-Table-In-White-Speckle/46368979';
        const mockBrowser = {
            newContext: jest.fn().mockImplementation(() => ({
                newPage: jest.fn().mockImplementation(() => ({
                  title: jest.fn().mockResolvedValue('Product Name - Walmart.com')
                }))
              }))
        };
        scraper = new ProductScraper(testUrl, mockBrowser);
        scraper.page = mockBrowser.newContext().newPage();
        scraper.getHTML = jest.fn().mockResolvedValue('"upc":"012345678901"');
        scraper.page.$eval = jest.fn().mockResolvedValue('$60.00');
    });
    afterAll(async () => {
        // Close the browser after all tests
        await scraper.closeBrowser();
    });

    test('returns a product name', async () => {
        const name = await scraper.getProductName();
        expect(name).toMatch(/Product Name/);
    });

    test('returns a retailer', async () => {
        const retailer = await scraper.getRetailer();
        expect(retailer).toMatch(/Walmart.com/);
    });

    test('returns a upc', async () => {
        const html = await scraper.getHTML();
        const upc = await scraper.getUpc(html);
        expect(upc).toMatch(/[0-9]+/);
    });

    test('returns a price', async () => {
        const price = await scraper.getPrice();
        expect(price).toMatch('$60.00');
    });
});