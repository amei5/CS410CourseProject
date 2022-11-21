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

    results = []

    # skip first element since it's not an actual listing
    listings = soup.select('.s-item__wrapper.clearfix')[1:]

    for item in listings:
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
    #return items

    '''data = {
        'summary': wikipedia.summary(topic, sentences=1),
        'raw': 'Successful',
    }'''

    #print('json-data to be sent: ', data)

    return JsonResponse(result)