import requests

from bs4 import BeautifulSoup

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
}

base_url = 'https://www.ebay.com/sch/i.html?_nkw={}'

def getEbayResults(query):
    url = base_url.format(query)
    html = requests.get(url, headers=headers).text
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

        description = extractDescription(link)

        result = {
            'title': title,
            'link': link,
            'price': price,
            'description': description,
            'image': image,
        }

        results.append(result)    
        print(result)
    
    return results

# access item page and extract item's description
def extractDescription(link):
    if link == '':
        return ''
    item_html = requests.get(link, headers=headers).text
    item_soup = BeautifulSoup(item_html, 'lxml')
    iframe_src = item_soup.select_one("#desc_ifr").attrs['src']
    desc_html = requests.get(iframe_src,headers=headers).text
    desc_soup = BeautifulSoup(desc_html, 'lxml')

    try:
        desc = desc_soup.find('div', id='ds_div').text.strip()
    except:
        desc = ''
    
    return desc


if __name__ == '__main__':
    query = user_input = input("Search for: ")
    query = query.strip()
    results = getEbayResults(query)

