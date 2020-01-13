def scrape():

    import os
    import pandas as pd
    from splinter import Browser
    from bs4 import BeautifulSoup
    import requests

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    results = soup.find_all('li', class_='slide')
    one = results[0].find('div',class_ = "content_title")
    news_title = one.find('a').text
    par = results[0].find('div',class_ = "article_teaser_body").text

    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    browser.click_link_by_partial_href('/spaceimages/images/largesize')
    featured_image_url = browser.url

    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    html3 = browser.html
    soup3 = BeautifulSoup(html3,'html.parser')
    weather_results = soup3.find_all('div',class_ = 'js-tweet-text-container')
    weather_text = weather_results[0].find('p')
    weather_img = weather_text.find('a','twitter-timeline-link').text
    mars_weather = (weather_text.text).strip(weather_img)

    url4 = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(url4)
    mars_facts_html = mars_facts[0].to_html

    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)
    html5 = browser.html
    soup5 = BeautifulSoup(html5,'html.parser')
    hemis = soup5.find_all('div',class_ = 'description')
    titles = []
    for hemi in hemis:
        title = hemi.find('h3').text
        titles.append(title)
    urls = []
    for link in titles:
        browser.click_link_by_partial_text(link)
        htmlloop = browser.html
        urlloop = BeautifulSoup(htmlloop,'html.parser')
        loop1 = urlloop.find('div',class_ = 'downloads')
        loop2 = loop1.find('a')['href']
        urls.append(loop2)
        browser.visit(url5)
    hemisphere_urls = {}
    for key in titles:
        for value in urls:
            hemisphere_urls[key] = value
            urls.remove(value)
            break

    final_dict = {'news_title':news_title,
                    'news_p': par,
                    'featured_image_url':featured_image_url,
                    'weather':mars_weather,
                    'html_table':mars_facts_html,
                    'hemisphere_image_urls':hemisphere_urls}
    print(final_dict)
    return final_dict
    