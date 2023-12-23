# **Issac's** **Index**
<img src=".readme_photos\issacs_index_logo.jpeg" width="200">

## Table of Contents

- [Senior Project](#senior-project)
- [App Description](#app-description)
- [Issac's Insight](#issacs-insight)
- [Methodology](#methodology)
  - [Languages](#languages)
  - [Website](#website)
  - [Chrome Extension](#chrome-extension)
  - [Database](#database)
  - [Deployment Method](#deployment-method)
- [Environment Setup](#environment-setup)
- [Getting Started](#getting-started)
- [Testing Frameworks](#testing-frameworks)
- [Future Work](#future-work)
- [System Diagram](#system-diagram)
- [UI Screenshots](#ui-screenshots)
- [Environment Variables](#environment-variables)
- [Links](#links)
- [Authors](#authors)

## Senior Project <a name="senior-project"></a>
This is a semester-long senior project carried out by a team of four dedicated students following the Agile Scrum methodology. Unfortunately, our fifth classmate, Issac, was unable to join the class due to scheduling conflict. We named the project after him to honor his contribution to the project.

## App Description <a name="app-description"></a>
Issac's Index is a price and review aggregator extension designed to enhance your online shopping experience. When you're on a product page, our extension will conveniently display prices for the same product from various retailers, ensuring that you can make an informed purchase at the most affordable price. Additionally, the website will curate user reviews from different retailers, eliminating irrelevant and fake ones, and provide a "Issac's Insight" score, akin to the popular Rotten Tomatoes rating system. This score will help you make more confident buying decisions based on the collective wisdom of fellow shoppers.

## Issac's Insight <a name="issacs-insight"></a>
Isaac's Insight provides invaluable insights to users by searching and extracting key similar and identical product data points from countless online retailers. This aggregated score is dynamically calculated and consistently updated with each request, enhancing users' online shopping experience in this ever-changing online retail landscape. 

## Methodology <a name="methodology"></a>

#### Languages: <a name="languages"></a>
- Python
- JavaScript
- HTML
- CSS
- SQL

#### Website: <a name="website"></a>
- Flask
- SQLAlchemy
- Bootstrap

#### Chrome Extension: <a name="chrome-extension"></a>
- Node.js 
- Playwright
- BootStrap

#### Database: <a name="database"></a>
- PostgreSQL

#### Deployment Method: <a name="deployment-method"></a>
- Cloud Deployed using Heroku

## Environment Setup <a name="environment-setup"></a>

1. Linux:
    - Ensure that you have a Linux distribution installed on your system. If you don't already have one, you can choose from popular distributions like Ubuntu, Fedora, or Debian and follow their respective installation instructions.

2. Install Python and Pip:
    - Make sure you have Python and Pip installed on your Linux distribution.

3. Clone the Repository

4. Install Python Dependencies:

    - ```pip install -r requirements.txt```

Now, your development environment on Linux is set up and ready to go. You can start working on Issac's Index with the required tools and packages in place.

## Getting Started <a name="getting-started"></a>

To use Issac's Index Chrome extension, follow these steps:

1. Open Google Chrome and navigate to the Chrome Extensions page by entering the following URL in the address bar: chrome://extensions/.

2. Enable Developer Mode by toggling the switch in the top right corner of the Extensions page.

3. Click on the "Load unpacked" button.

4. In the file dialog that appears, navigate to the directory where you have the repository for Issac's Index saved.

5. Inside the repository folder, select the "chrome extension" folder (not the entire repository).

6. Click "Open" to load the extension.

7. Once the extension is loaded, you'll see its icon in your Chrome extension bar.

8. Now, visit Walmart's website and navigate to a product page. The extension will automatically activate and display price comparisons and other relevant information, making your online shopping experience more convenient and cost-effective.

Enjoy using Issac's Index to find the best prices and reviews while shopping online!

## Testing Frameworks <a name="testing-frameworks"></a>
- Pytest
- Jest

Test coverage - 71%

## Future Work <a name="future-work"></a>
- Screen for fake reviews
- Activate on any retailer webpage
- Price history
- Customizable Insight score

## System Diagram <a name="system-diagram"></a>
<img src=".readme_photos\issacs_index_system_diagram.png" width="1000"> 

## UI Screenshots <a name="ui-screenshots"></a>

### Chrome Extension
<img src=".readme_photos\issacs_index_ce_1.png" width="600"> 
<img src=".readme_photos\issacs_index_ce_2.png" width="600"> 
<img src=".readme_photos\issacs_index_ce_3.png" width="600"> 
<img src=".readme_photos\issacs_index_ce_4.png" width="600"> 

### Website
<img src=".readme_photos\issacs_index_website_1.png" width="700"> 
<img src=".readme_photos\issacs_index_website_2.png" width="700"> 


## Enviroment Variables <a name="environment-variables"></a>

Add ".env" to your .gitignore file. Create a .env file in the projects root folder. Put the following variables in the .env file. Never expose your secrets!

| Description | Variables                                |
| :---        | :---                                     |
| Serp API    | SERP_API_KEY=your_actual_api_key_here    |


All Enviroments are shared through 1Pass. Access through shared the Vault "issacs-index-env-variables". Email Jesse for access (jesse.d.johnson.533@gmail.com). 

## Authors <a name="authors"></a>
<img src=".readme_photos\isaac_throbber.gif" width="50"> 

**Ryan Guyton** 

- [Github](https://github.com/NeurotikPsyntist "Ryan Guyton") 
- ryan.r.guyton@tutanota.com

**Jesse Johnson**

- [Github](https://github.com/JesseJohnson533 "JesseJohnson533")
- jesse.d.johnson.533@gmail.com

**Nathan Mead**

- [Github](https://github.com/nmead1 "Nathan Mead")
- meadnl89@gmail.com

**Mitchell Thompson**

- [Github](https://github.com/MitchellThompson1 "Mitchell Thompson")
- MitchellLoganThompson@gmail.com

<img src=".readme_photos\isaac_throbber.gif" width="50"> 
