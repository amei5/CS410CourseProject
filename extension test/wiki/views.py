from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
import json
from django.contrib.auth.models import User #####
from django.http import JsonResponse , HttpResponse ####

#import wikipedia
import requests
import lxml
from bs4 import BeautifulSoup
import cchardet

def index(request):
    return HttpResponse("Hello, world. You're at the ebay index.")


# https://pypi.org/project/wikipedia/#description
def get_ebay_summary(request):
    topic = request.GET.get('topic', None)
    base_url = "https://www.ebay.com/sch/i.html?_nkw={}"

    print('topic:', topic)
    url = base_url.format(topic)
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')

    items = []

    for item in soup.select('.s-item__wrapper.clearfix')[1:]:
        title = item.select_one('.s-item__title').text

        link = item.select_one('.s-item__link')['href']

        item_html = requests.get(link).text
        item_soup = BeautifulSoup(item_html, 'lxml')

        iframe_src = item_soup.select_one("#desc_ifr").attrs["src"]
        desc_html = requests.get(iframe_src).text
        desc_soup = BeautifulSoup(desc_html, 'lxml')
        desc = desc_soup.find('div', id='ds_div').text.strip()

        try:
            image = item.select_one('.s-item__image-img')['src']
        except:
            image = None

        try:
            price = item.select_one('.s-item__price').text
        except:
            price = None

        items = {
            "title": title,
            'link': link,
            "price": price,
            'description': desc,
            'image': image,
        }

    #return items

    '''data = {
        'summary': wikipedia.summary(topic, sentences=1),
        'raw': 'Successful',
    }'''

    #print('json-data to be sent: ', data)

    return JsonResponse(items)