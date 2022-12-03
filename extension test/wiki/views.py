from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.contrib.auth.models import User #####
from django.http import JsonResponse , HttpResponse ####

import requests
from requests import get
from bs4 import BeautifulSoup
import re

def index(request):
    return HttpResponse("Hello, world. You're at the ebay index.")


def get_ebay_summary(request):
    topic = request.GET.get('topic', None)
    ebay_url = "https://www.ebay.com/sch/i.html?_nkw={}"
    poshmark_url = "https://poshmark.com/search?query="
    goodwill_url = "https://www.goodwillfinds.com/search/?q="

    results = []

    print('topic:', topic)

    # goodwill results

    driver = get(goodwill_url + topic)  # Getting page HTML through request
    soup = BeautifulSoup(driver.text,
                         'lxml')  # Parsing content using beautifulsoup. Notice driver.page_source instead of page.content

    gw_results = soup.select("p.b-product_tile-title a")
    prices_list = soup.select("div.b-product_tile-price span.b-price")
    images = soup.select(
        "div.b-product_tile-top a.b-product_tile_images-link picture.b-product_tile_images-item source")

    for title in gw_results[:3]:
        results.append({
            "title": title.text
        })

    i = 0
    for link in gw_results[:3]:
        link_to_prod = "https://www.goodwillfinds.com/" + link['href']
        results[i]["link"] = link_to_prod
        i = i + 1

    i = 0
    for price in prices_list[:3]:
        results[i]["price"] = price.text.strip(' \n\t').split()[3]
        i = i + 1

    i = 0
    for image in images:
        if i < len(results):
            image_link = image['srcset']
            results[i]["image"] = image_link
        else:
            break
        i = i + 1

    #get ebay results

    url = ebay_url.format(topic)
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')

    # skip first element since it's not an actual listing
    listings = soup.select('.s-item__wrapper.clearfix')[1:]

    for item in listings[:3]:
        try:
            title = item.select_one('.s-item__title').text
        except:
            title = ''

        try:
            link = item.select_one('.s-item__link')['href']
        except:
            link = ''

        try:
            image = item.select_one('.s-item__image-img')['src']
        except:
            image = ''

        try:
            price = item.select_one('.s-item__price').text
        except:
            price = ''

        result = {
            "title": title,
            'link': link,
            "price": price,
            'image': image,
        }
        results.append(result)

    #get poshmark results
    page = get(poshmark_url + topic + "&type=listings&src=dir")
    soup = BeautifulSoup(page.text, 'lxml')
    item_tiles = soup.find_all('div', class_='col-x12')

    for tile in item_tiles[:3]:
        try:
            title = tile.find('a', class_='tile__title').get_text(strip=True)
        except:
            title = ''

        try:
            price_string = tile.find('span', class_="fw--bold").get_text(strip=True)
            price = int(price_string.replace('$', ''))
        except:
            price = ''

        try:
            partial_link = tile.find('a', class_='tile__title').get('href')
            link = 'http://www.poshmark.com' + partial_link
        except:
            link = ''

        try:
            image = tile.find('img')['src']
        except:
            image = ''

        result = {
            'title': title,
            'price': price,
            'link': link,
            'image': image,
        }
        results.append(result)

    # filter out results that do not contain the search topic words
    filtered_results = []
    for result in results:
        print(result['title'])
        topic_words = topic.lower().split(' ')
        title_words = result['title'].lower().split(' ')

        topic_word_missing = False
        for word in topic_words:
            if word not in result['title'].lower():
                topic_word_missing = True   
        
        title_words_in_topic_substrings = []
        for word in title_words:
            if word in topic.lower():
                title_words_in_topic_substrings.append(word)
        

        if not topic_word_missing or len(title_words_in_topic_substrings) == len(topic_words):
            filtered_results.append(result)
    
    results = filtered_results


    # Extract the integer from the string price values in the results array, and sort by lowest to highest price
    for result in results:
        if type(result['price']) == int:
            continue
        result['price'] = float(re.findall("\d+\.\d+", result['price'])[0])

    def customSort(k):
        return k['price']

    results.sort(key=customSort)
    print(results)

    return JsonResponse(results, safe=False)
