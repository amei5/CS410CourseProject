from bs4 import BeautifulSoup
from selenium import webdriver

option = webdriver.ChromeOptions()
option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-sh-usage')
driver = webdriver.Chrome('/chromedriver', options=option)

def get_good_will_results(query):
    driver.get('https://www.goodwillfinds.com/search/?q=' + query)  # Getting page HTML through request
    soup = BeautifulSoup(driver.page_source, 'html.parser')  # Parsing content using beautifulsoup. Notice driver.page_source instead of page.content

    results = soup.select("p.b-product_tile-title a")
    product_category = soup.select("div.b-product_tile-category_size")
    prices_list = soup.select("div.b-product_tile-price span.b-price")

    #results = result[:5]  # Keep only the first 10 anchors
    #product_category = product_category_size[:5]
    #prices_list = prices[:5]

    goodwill_results = []
    for title in results:
        goodwill_results.append({
            "Title": title.text
        })

    i = 0
    for link in results:
        link_to_prod = "https://www.goodwillfinds.com/" + link['href']
        goodwill_results[i]["Link"] = link_to_prod
        i = i + 1

    i = 0
    for category in product_category:
        goodwill_results[i]["Category"] = category.text.strip(' \n\t').split()[3]
        i = i+1

    i = 0
    for price in prices_list:
        goodwill_results[i]["Price"] = price.text.strip(' \n\t').split()[3]
        i = i + 1

    return goodwill_results

if __name__ == '__main__':
    # Here is an example query
    query = "sweaters"
    results = get_good_will_results(query)
    # Printing results so its easy to check the output format
    for result in results:
        print(result)
    # Sample output format - array of objects with each object giving details about a result: "{'Title': 'The Italian Sweater Men Vest Grey L', 'Link': 'https://www.goodwillfinds.com//men/sweaters/vest/the-italian-sweater-men-vest-grey-l/10014-0000-53498.html', 'Category': 'Men', 'Price': '$18.00'}"