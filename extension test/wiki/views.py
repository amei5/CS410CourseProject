from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
import json
from django.contrib.auth.models import User #####
from django.http import JsonResponse , HttpResponse ####

import requests
from requests import get
import lxml
from bs4 import BeautifulSoup
import cchardet

def index(request):
    return HttpResponse("Hello, world. You're at the ebay index.")


def get_ebay_summary(request):
    topic = request.GET.get('topic', None)
    ebay_url = "https://www.ebay.com/sch/i.html?_nkw={}"
    poshmark_url = "https://poshmark.com/search?query=jeans&type=listings&src=dir"
    goodwill_url = "https://www.goodwillfinds.com/search/?q="

    results = []

    print('topic:', topic)

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
    page = get(poshmark_url)
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
            image = tile.find('img').get('data-src')
        except:
            image = ''

        result = {
            'title': title,
            'price': price,
            'link': link,
            'image': image,
        }
        results.append(result)

    goodwill_page = get(goodwill_url + topic)  # Getting page HTML through request
    soup = BeautifulSoup(goodwill_page.text,'lxml')

    gw_results = soup.select("p.b-product_tile-title a")
    product_category = soup.select("div.b-product_tile-category_size")
    prices_list = soup.select("div.b-product_tile-price span.b-price")

    return JsonResponse(results, safe=False)
'''
    for listing in gw_results[:3]:
        title = listing.text
        link = "https://www.goodwillfinds.com/" + listing['href']
        price = listing.text.strip(' \n\t').split()[3]

            result = {
                'title': title,
                'price': price,
                'link': link,
             }
            results.append(result)
'''
