# Dependencies
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def scrape():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URLS
    mars_news_url = "https://redplanetscience.com/"
    space_images_url = "https://spaceimages-mars.com/"
    mars_facts_url = "https://galaxyfacts-mars.com/"
    mars_geo_url = "https://marshemispheres.com/"

    # 1. Mars News
    browser.visit(mars_news_url)
    news_html = browser.html
    news_soup = BeautifulSoup(news_html, 'html.parser')
    news_date = news_soup.find("div",{"class":"list_date"}).text
    news_title = news_soup.find("div",{"class":"content_title"}).text
    news_desc = news_soup.find("div",{"class":"article_teaser_body"}).text

    # 2. Featured Image
    browser.visit(space_images_url)
    space_image_html = browser.html
    image_soup = BeautifulSoup(space_image_html, 'html.parser')
    image_src = image_soup.find("img", {"class":"headerimage"})["src"]
    image_url = space_images_url + image_src

    # 3. Mars Facts
    mars_facts_table = pd.read_html(mars_facts_url)[0] #get table
    mars_facts_table.columns = mars_facts_table.iloc[0]
    mars_facts_table.drop(index=0, inplace=True)
    mars_facts_table.set_index("Mars - Earth Comparison",inplace=True)
    facts_html = mars_facts_table.to_html()
    mars_facts_table.head()

    # 4. High Res Photos
    browser.visit(mars_geo_url)
    hemisphere_image_urls = list()
    geo_html = browser.html
    geo_soup = BeautifulSoup(geo_html, 'html.parser')
    geo_links = geo_soup.find_all("a", {"class", "itemLink product-item"}) #get all the links
    endpoints = set([link["href"] for link in geo_links]) #get the url enpoints
    endpoints.remove("#")
    for point in endpoints:
        browser.visit(mars_geo_url+point)
        point_soup = BeautifulSoup(browser.html, "html.parser")
        image_src = point_soup.find("img", {"class" : "wide-image"})["src"]
        image_title = point_soup.find("h2", {"class" : "title"}).text
        hemisphere_image_urls.append({
            "title" : image_title,
            "img_url" : mars_geo_url+image_src})

    # Shut down Browser
    browser.quit()
    
    # Collate Return values
    scrape_return = {
        "mars_news" : { 
            "date" : news_date,
            "title" : news_title,
            "description" : news_desc},
        "featured_image_url" :  image_url,
        "facts_html_table" : facts_html,
        "high_res_photos" : hemisphere_image_urls
    }
    return scrape_return