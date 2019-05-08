from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import re
from sqlalchemy import create_engine
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


def scrape():
    marsFactsDict = {}

    baseUrl = "https://mars.nasa.gov/news/"
    browser.visit(baseUrl)
    html = browser.html
    soup = bs(html,"html.parser")
    """
    ### NASA Mars News

    * Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) 
    and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
    """
    newsTitle = soup.find("div",class_="content_title").text
    newsParagraph = soup.find("div", class_="article_teaser_body").text
    print(f"Title: {newsTitle}")
    print(f"Para: {newsParagraph}")
    marsFactsDict['newsTitle'] = newsTitle
    marsFactsDict['newsParagraph'] = newsParagraph

    """
    ### JPL Mars Space Images - Featured Image

    * Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).

    * Use splinter to navigate the site and find the image url for the current 
    Featured Mars Image and assign the url string to a variable called `featured_image_url`.

    * Make sure to find the image url to the full size `.jpg` image.

    * Make sure to save a complete url string for this image.
    """
    import time 

    baseUrlImage = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(baseUrlImage)
    html = browser.html
    soup = bs(html,"html.parser")
    xpath= "//*[@id=\"full_image\"]"
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()
    time.sleep(10)
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    # Wait for 5 seconds
    time.sleep(10)
    
    img_url = soup.find("img", class_="fancybox-image")["src"]
    full_img_url =  img_url
    print(full_img_url)
    from urllib.parse import urljoin
    full_img_url = urljoin(baseUrlImage, img_url)
    print(full_img_url)

    marsFactsDict['imageUrl'] = full_img_url
    """
    * Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. 
    Save the tweet text for the weather report as a variable called `mars_weather`.
    """
    urlWeather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(urlWeather)
    htmlWeather = browser.html
    soup = bs(htmlWeather, "html.parser")
    #temp = soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(mars_weather)
    marsFactsDict['mars_weather'] = mars_weather

    """
    * Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

    * Use Pandas to convert the data to a HTML table string.
    """

    urlFacts = "https://space-facts.com/mars/"
    table = pd.read_html(urlFacts)
    print(table)
    table[0]
    df_mars_facts = table[0]
    df_mars_facts.columns = ["Params", "Vals"]
    df_mars_facts.set_index(["Params"])
    mars_html_table = df_mars_facts.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_html_table
    marsFactsDict['htmlMarsData'] = mars_html_table

    """
    ### Mars Hemispheres

    * Visit the USGS Astrogeology site [here]
    (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)
    to obtain high resolution images for each of Mar's hemispheres.

    * You will need to click each of the links to the hemispheres in order to find the image url to 
    the full resolution image.

    * Save both the image url string for the full resolution hemisphere image, and the Hemisphere 
    title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.

    * Append the dictionary with the image url string and the hemisphere title to a list. 
    This list will contain one dictionary for each hemisphere.

    """

    hemisphere_img_urls = []
    for x in range(1,5):
        print(x)
        url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url_hemisphere)
        time.sleep(3)
        urlToClick = "//*[@id='product-section']/div[2]/div["+str(x)+"]/a/img"
        results = browser.find_by_xpath(urlToClick).click()
        time.sleep(3)
        localLink_open_click = browser.find_by_xpath( "//*[@id='wide-image-toggle']").click()
        time.sleep(3)
        localLink_image = browser.html
        soup = bs(localLink_image, "html.parser")
        localLink_url = soup.find("img", class_="wide-image")["src"]
        localLink_img_url = urljoin(url_hemisphere, localLink_url) 
        print(localLink_img_url)
        localLink_title = soup.find("h2",class_="title").text
        print(localLink_title)
        localLink = {"image title":localLink_title, "image url": localLink_img_url}
        hemisphere_img_urls.append(localLink)

    marsFactsDict['imageUrls'] = hemisphere_img_urls
    browser.quit()
    print(marsFactsDict)
    return marsFactsDict


if __name__ == '__main__':
    scrape()