# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from selenium import webdriver
import pandas as pd
import time

def init_browser():
  
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    
    browser = init_browser()

    scraped_mars = {}

    # NASA Mars News

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.select_one('ul.item_list li.slide')
    news_title = title.find('div', class_='content_title').get_text()
    paragraph = title.find('div', class_='article_teaser_body').get_text()
    date = title.find('div',class_='list_date').get_text()

    scraped_mars['news_title'] = news_title
    scraped_mars['news_paragraph'] = paragraph
    scraped_mars['news_date']= date

    # JPL Mars Space Images - Featured Image

    url1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url1)

    time.sleep(1)
    
    browser.click_link_by_partial_text('FULL IMAGE')

    time.sleep(1) 

    browser.is_element_present_by_text('more info')
    more_info = browser.find_link_by_partial_text('more info')
    more_info.click()

    time.sleep(1)

    html = browser.html
    soup1 = BeautifulSoup(html, 'html.parser')

    large_img = soup1.select_one('figure.lede a img').get("src")
    featured_image_url = f"https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars{large_img}"

    scraped_mars['featured_image_url'] = featured_image_url

    # Mars Weather

    url2 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url2)

    time.sleep(1)

    html = browser.html
    soup2 = BeautifulSoup(html, 'html.parser')
    mars_weather = soup2.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text

    scraped_mars['mars_weather'] = mars_weather

    # Mars Facts

    url3 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url3)
    df = tables[0]
    Mars_df = df.rename(columns={0:"Planet Characteristics", 1: "Value"})
    Mars_df.set_index("Planet Characteristics", inplace=True)
    Mars_Facts = Mars_df.to_html(justify='left')

    scraped_mars['mars_facts'] = Mars_Facts

    # Mars Hemispheres

    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    # html = browser.html
    # soup4 = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []

    hemis = browser.find_by_css('a.product-item h3')

    
    for h in range(len(hemis)):
    
        hem = {}
    
        browser.find_by_css('a.product-item h3')[h].click()
    
        partial_link = browser.find_link_by_text('Sample').first
        hem['img_url'] = partial_link['href']

        hem['title'] = browser.find_by_css('h2.title').text
    
        hemisphere_image_urls.append(hem)
    
        browser.back()

    scraped_mars['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()

    return scraped_mars
