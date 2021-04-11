# Import Splinter, BeautifulSoup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt 

# Set executable path and set up URL for scraping with Splinter
# Initiate headless driver for deployment
def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    # Set news title and paragraph variables
    news_title, news_paragraph = mars_news(browser)
    # # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_image_urls": hemisphere_image_urls(browser)
    }
    # Ending automated browsing session
    browser.quit()
    return data

# Aritcle Scraping

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # set up HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

# Image Scraping

# Featured Images
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # We'll use the image tag and class (<img />and fancybox-img) to build the URL to the full-size 
    # image.
    # Find the relative image url & Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

# Scraping Mars Facts
def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    return df.to_html()

# Scraping hemisphere data
def hemisphere_image_urls(browser):
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    # HTML object
    html = browser.html
    # Parse HTML with BeautifulSoup
    hemis_soup = soup(html, 'html.parser')
    # Retrieve all elements that contain hemisphere image info
    hem_img = hemis_soup.find_all('div', class_='description')
    #Iterate through each hemisphere image
    for mars_img in hem_img:
        # Find url
        hem_url = mars_img.find('a', class_='itemLink').get('href')
        hem_link = f'https://astrogeology.usgs.gov/{hem_url}'
    
        #Go to each hem_link
        browser.visit(hem_link)
    
        # Parse each hem_link
        mars_html = browser.html
        mars_hemis_soup = soup(mars_html, 'html.parser')
    
        #Retrieve image URL
        img_url = mars_hemis_soup.find('a', text='Sample').get('href')
    
        # Retrieve title
        title = mars_hemis_soup.find('h2', class_='title').text
    
        # Create dictionary to hold image url and title
        hemispheres = {"img_url": img_url,
                        "title": title}
    
        # Append dictionaries to list
        hemisphere_image_urls.append(hemispheres)
    
    return hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())










