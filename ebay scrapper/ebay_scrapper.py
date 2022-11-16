import lxml
import requests

from bs4 import BeautifulSoup

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

base_url = "https://www.ebay.com/sch/i.html?_nkw={}"

def getEbayResults(query):
    url = base_url.format(query)
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')

    items = []

    for item in soup.select('.s-item__wrapper.clearfix')[1:]:
        title = item.select_one('.s-item__title').text

        link = item.select_one('.s-item__link')['href']
        
        item_html = requests.get(link, headers=headers).text
        item_soup = BeautifulSoup(item_html, 'lxml')

        iframe_src = item_soup.select_one("#desc_ifr").attrs["src"]
        desc_html = requests.get(iframe_src,headers=headers).text
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

        items.append({
            "title": title,
            'link': link,
            "price": price,
            'description': desc,
            'image': image,
        })
    
    return items


if __name__ == '__main__':
    query = user_input = input("Search for: ")
    query = query.strip()
    getEbayResults(query)

