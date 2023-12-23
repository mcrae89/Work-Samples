// content.test.js
describe('content.js tests', () => {
    let chrome;

    beforeEach(() => {
        // Check if window is defined
        if (typeof window === 'undefined') {
           global.window = {};
        }

        // Mock window.location.href
        delete global.window.location;
        global.window.location = {
            href: 'https://test.url'
        };

        // Mock chrome.runtime.sendMessage
        chrome = {
            runtime: {
                sendMessage: jest.fn()
            }
        };
        global.chrome = chrome;
    });

    test('sends a message with the current URL', () => {
        require('../../../chrome_extension/content.js');

        expect(chrome.runtime.sendMessage).toHaveBeenCalledWith({ action: "fetchData", url: 'https://test.url' });
    });
});