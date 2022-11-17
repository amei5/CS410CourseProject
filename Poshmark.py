from bs4 import BeautifulSoup
from requests import get


def download_page(url):
    response = get(url)
    return response

def create_soup(source):
    soup = BeautifulSoup(source.text, 'html.parser')
    return soup

def extract_tiles(soup):
    containers = soup.find_all('div', class_ = 'col-x12')
    return containers

def extract_title(tile):
    title = tile.find('a', class_='tile__title').get_text(strip=True)
    return title

def extract_price(tile):
    price_string = tile.find('span', class_="fw--bold").get_text(strip=True)
    price = int(price_string.replace('$', ''))
    return price

def extract_link(tile):
    partial_link = tile.find('a', class_='tile__title').get('href')
    link = 'http://www.poshmark.com' + partial_link
    return link

def extract_image(tile):
    image = tile.find('img').get('data-src')
    return image
    

def combine_data(tile):
    try:
        title = extract_title(tile)
    except:
        title = ''
        
    try:
        price = extract_price(tile)
    except: 
        price = ''
    
    try: 
        link = extract_link(tile)
    except:
        link = ''
        
    try:
        image = extract_image(tile)
    except:
        image = ''
        
    return {
        'title': title,
        'price': price,
        'link': link,
        'image': image,
    }

url = "https://poshmark.com/search?query=jeans&type=listings&src=dir"

page = download_page(url)
soup_obj = create_soup(page)
item_tiles = extract_tiles(soup_obj)
item_objs = [combine_data(tile) for tile in item_tiles]

print(len(item_objs))
print(item_objs[0])
