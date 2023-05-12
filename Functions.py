from pprint import pprint
import requests
from bs4 import BeautifulSoup

url_book = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
domain = 'http://books.toscrape.com/'


def html_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def one_book_data(url):
    response = html_content(url)
    product_page_url = url
    table = response.find('table', {'class': 'table table-striped'}).find_all('td')
    upc = table[0].string
    title = response.find('title').string.strip()
    ttc = table[3].string
    ht = table[2].string
    availability = table[5].string.split()[2].replace('(', '')
    div_product_description = response.find('div', {'id': 'product_description'})
    try:
        product_description = div_product_description.find_next_sibling().string
    except TypeError:
        product_description = ''
    category = response.find('ul', {'class': 'breadcrumb'}).find_all('a')[2].string.strip()
    rating_str = response.find('p', {'class': 'star-rating'})['class'][1]
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    review_rating = rating_map[rating_str]
    image_url = f"{domain}{response.find('img')['src'].strip('./')}"

    print(f"URL : {product_page_url}")
    print(f"UPC: {upc}\nTitle: {title}\nTTC: {ttc}\nHT: {ht}\nAvailability: {availability}\nCategory: {category}\n"
          f"Review Rating: {review_rating}\n")
    pprint(f" {product_description}")
    print(image_url)


one_book_data(url_book)
