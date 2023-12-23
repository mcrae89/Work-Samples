const { chromium } = require('playwright-extra');
const stealth = require('puppeteer-extra-plugin-stealth')();
chromium.use(stealth);

class ProductScraper {
  constructor(url, browser = null) {
    this.url = url;
    this.browser = browser;
  }

  async initializeBrowser() {
    if (!this.browser) {
      this.browser = await chromium.launch();
    }
    const context = await this.browser.newContext();
    this.page = await context.newPage();
  }

  async navigatePage() {  
    try {
      await this.page.goto(this.url);
    } catch (error) {
      console.error(`Failed to navigate to ${this.url}`, error);
    }
  }
  
  // Evaluate JavaScript, load HTML
  async getHTML() {
    const body = await this.page.evaluateHandle(() => document.body);
    const bodyHTML = await this.page.evaluateHandle(body => body.outerHTML, body);
    const bodyHTMLText = await bodyHTML.jsonValue();
    return bodyHTMLText;
  }

  // Pull product name from title tag and clean up
  async getProductName() {
    const title = await this.page.title();
    var productName = null;
    if (title.match(/:(.*?)\-/)) {
      productName = title.match(/:(.*?)\-/)[1].trim();
    } else if (title.match(/(.*?)\-/)) {
      productName = title.match(/(.*?)\-/)[1].trim();
    } else {
      console.log('No productName match')
    }
    return productName;
  }

  // Pull retailer from title tag
  async getRetailer() {
    const title = await this.page.title();
    var retailer = null;
    if (title.match(/(\w+).com$/)) {
      retailer = title.match(/(\w+).com$/)[0].trim();
    } else if (title.match(/(\w+)$/)) {
      retailer = title.match(/(\w+)$/)[0].trim();
    } else {
      console.log('No retailer match')
    }
    return retailer;
  }

  // Pull UPC from HTML
  async getUpc(bodyHTMLText) {
    const upcMatch = bodyHTMLText.match(/"upc":"[0-9]+"/);
    var upc = null;
    if (upcMatch) {
      upc = upcMatch[0].substring(7, upcMatch[0].length - 1);
    }
    return upc;
  }

  // Pull price from HTML
  async getPrice() {
    const price = await this.page.$eval('span[itemprop="price"]', el => el.textContent);
    return price;
  }

  // Close browser
  async closeBrowser() {
    if (this.browser && typeof this.browser.close === 'function') {
        await this.browser.close();
    }
  }
}

// Main function to run scraper
async function main(currentUrl) {
  const scraper = new ProductScraper(currentUrl);
  await scraper.initializeBrowser();
  await scraper.navigatePage();
  const bodyHTML = await scraper.getHTML();
  const product = {
    "productName": await scraper.getProductName(),
    "retailer": await scraper.getRetailer(),
    "upc": await scraper.getUpc(bodyHTML),
    "price": await scraper.getPrice()
  };
  await scraper.closeBrowser();
  
  const jsonProduct = JSON.stringify(product);
  
  return jsonProduct;
}

// Current URL sent from Chrome extension
// const defaultUrl = 'https://www.walmart.com/ip/Cosco-6-Foot-Folding-Table-In-White-Speckle/46368979';
const defaultUrl = 'https://www.walmart.com/ip/Apple-iPhone-8-Plus-256GB-Silver-Verizon-Unlocked-USED-Grade-A/560458842';
const currentUrl = process.argv[2] || defaultUrl;

if (!currentUrl) {
  console.error('No URL provided');
  process.exit(1);
}

main(currentUrl).then((product) => {
  console.log(product);
});

// Export class for testing
module.exports.ProductScraper = ProductScraper;