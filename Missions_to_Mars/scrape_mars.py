from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

   # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'


    browser.visit(url)


    # Create BeautifulSoup object; parse with 'lxml'    
    html = browser.html
    soup = bs(html, 'lxml')

    # Extract the title of the HTML document
    title = soup.find_all("div", class_="content_title")
    title = title[1].get_text()
    title

    paragraph = soup.find_all("div", class_="article_teaser_body")
    paragraph = paragraph[0].get_text()
    paragraph

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    full_image = browser.find_by_id("full_image")
    full_image.click()
    time.sleep(1)
    more_info = browser.links.find_by_partial_text("more info")
    more_info.click()

    html = browser.html
    time.sleep(2)
    feature = bs(html, "html.parser")
    image_url = feature.select_one('figure.lede a img').get("src")
    image_url = "https://www.jpl.nasa.gov" + image_url 
    image_url

    #Scrape table containing facts about the planet Diameter, Mass, etc.  Convert the data to a HTML table string. https://space-facts.com/mars/
    fact_url = "https://space-facts.com/mars"
    df = pd.read_html(fact_url) 
    df = df[0]
    df.columns = ["description", "mars"]
    

    mars_table = df.to_html()

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemisphere_url = browser.links.find_by_partial_text("Enhanced")
    len(hemisphere_url)

    hemisphere_list = []
    for i in range(len(hemisphere_url)):
        hemisphere = {}
        browser.links.find_by_partial_text("Enhanced")[i].click()
        sample = browser.links.find_by_text("Sample").first
        hemisphere["img_url"] = sample["href"]
        hemisphere["title"] = browser.find_by_css("h2.title").text
        hemisphere_list.append(hemisphere)
        browser.back()
    hemisphere_list


    # Store data in a dictionary
    mars_data = {
        "title": title,
        "paragraph": paragraph,
        "feature": image_url,
        "mars_table": mars_table,
        "hemisphere": hemisphere_list
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data