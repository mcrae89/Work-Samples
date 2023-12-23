// content.js
const currentUrl = window.location.href;
console.log('Current URL:', currentUrl);

chrome.runtime.sendMessage({ action: "fetchData", url: currentUrl });
