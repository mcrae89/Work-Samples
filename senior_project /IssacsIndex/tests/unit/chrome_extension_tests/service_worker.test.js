// service_worker.test.js

global.fetch = jest.fn();
global.chrome = {
    runtime: {
        onMessage: {
            addListener: jest.fn()
        },
        onInstalled: {
            addListener: jest.fn()
        }
    },
    tabs: {
        onUpdated: {
            addListener: jest.fn()
        },
        onRemoved: {
            addListener: jest.fn()
        }
    },
    storage: {
        local: {
            set: jest.fn((data, callback) => callback())
        }
    },
    notifications: {
        create: jest.fn()
    }
};

const {
    fetchScrapeData,
    handleData,
    postDataToAPI,
    extractPricesData,
    postPricesDataToAPI,
    triggerProductData
} = require('../../../chrome_extension/service_worker.js');

describe('Service Worker Tests', () => {
    beforeEach(() => {
        global.fetch.mockClear();
        global.chrome.runtime.onMessage.addListener.mockClear();
        global.chrome.storage.local.set.mockClear();
        global.chrome.notifications.create.mockClear();
    });

    test('fetchScrapeData makes a fetch request and returns data', async () => {
        const mockData = { productName: 'Product', upc: '12345', retailer: 'Retailer', price: '$60.00' };
        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: () => Promise.resolve(mockData)
        });

        const data = await fetchScrapeData('https://example.com');
        expect(data).toEqual({ ...mockData, source_url: 'https://example.com' });
        expect(global.fetch).toHaveBeenCalledTimes(1);
    });

    test('handleData posts data and triggers product data', async () => {
        const mockData = { productName: 'Product', upc: '12345', retailer: 'Retailer', price: '$60.00', source_url: 'https://example.com' };
        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: () => Promise.resolve({})
        }).mockResolvedValueOnce({
            ok: true,
            json: () => Promise.resolve({})
        }).mockResolvedValueOnce({
            ok: true,
            json: () => Promise.resolve({ message: 'Triggered Product Data' })
        });
       
        handleData(mockData);
        setTimeout(() => {
            expect(global.fetch).toHaveBeenCalledTimes(3);
            expect(global.chrome.storage.local.set).toHaveBeenCalledTimes(1); 
            expect(global.chrome.notifications.create).toHaveBeenCalledTimes(1);
            done();
        }, 1000);
    });

    test('postDataToAPI posts product data', async () => {
        const mockData = { productName: 'Product', upc: '12345', retailer: 'Retailer', price: '$60.00', source_url: 'https://example.com' };
        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: () => Promise.resolve({})
        });
    
        const data = await postDataToAPI(mockData);
        expect(data).toEqual({});
        expect(global.fetch).toHaveBeenCalledTimes(1);
    });

    test('extractPricesData extracts prices data', () => {
        const mockData = { productName: 'Product', upc: '12345', retailer: 'Retailer', price: '$60.00', source_url: 'https://example.com' };
        const pricesData = extractPricesData(mockData);

        expect(pricesData).toEqual({
            prices: [{
                product_name: 'Product',
                price: 60.00,
                retailer: 'Retailer',
                price_url: 'https://example.com'
            }],
            product_name: 'Product'
        });
    });

    test('postPricesDataToAPI posts prices data', async () => {
        const mockData = {
            prices: [{
                product_name: 'Product',
                price: 60.00,
                retailer: 'Retailer',
                price_url: 'https://example.com'
            }],
            product_name: 'Product'
        };
        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: () => Promise.resolve({})
        });
    
        await postPricesDataToAPI(mockData);
        expect(global.fetch).toHaveBeenCalledTimes(1);
    });

    test('triggerProductData triggers product data', async () => {
        const mockData = { productName: 'Product', upc: '12345', retailer: 'Retailer', price: '$60.00', source_url: 'https://example.com' };
        global.fetch.mockResolvedValueOnce({
            ok: true,
            text: () => Promise.resolve(JSON.stringify({ message: 'Triggered Product Data' }))
        });
    
        const data = await triggerProductData(mockData);
        expect(data).toEqual({ message: 'Triggered Product Data' });
        expect(global.fetch).toHaveBeenCalledTimes(1);
    });
});