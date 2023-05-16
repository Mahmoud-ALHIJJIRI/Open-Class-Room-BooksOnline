# Import required modules

import requests
from bs4 import BeautifulSoup
import csv


# Define the URL and domain name of the website
url_book = 'http://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html'
domain = 'http://books.toscrape.com/'
one_category_url = 'http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'


# Function to get the HTML content of a URL and parse it using BeautifulSoup
def html_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


# Function to extract the data of a book from its URL
def one_book_data(url):
    response = html_content(url)
    product_page_url = url
    # Find the table containing the data
    table = response.find('table', {'class': 'table table-striped'}).find_all('td')
    # Extract the required data from the table
    upc = table[0].string
    title = response.find('title').string.strip()
    price_including_tax = table[3].string
    price_excluding_tax = table[2].string
    number_available = table[5].string.split()[2].replace('(', '')
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

    # Return the extracted data as a tuple
    return product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available, \
        product_description, category, review_rating, image_url


# Function to write the data of a book to a CSV file
def write_book_data_to_csv(url):
    # Define the headers of the CSV file
    headers = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
               "number_available", "product_description", "category", "review_rating", "image_url"]

    # Get the title of the book from the URL
    title_book = (one_book_data(url)[2]).replace('|', '-')
    # Open the CSV file for writing and write the headers as the first row
    with open(title_book + '.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(headers)
        # Get the data for the book and write it to the CSV file
        book_data = one_book_data(url)
        writer.writerow(book_data)


def get_all_categories_names_and_url():

    response = html_content(domain)
    all_categories_url = []
    all_categories_names = []
    list_books = response.find('ul', {'class': 'nav nav-list'}).find('ul').find_all('li')
    for list_book in list_books:
        all_categories_url.append(f"{domain}" + list_book.a['href'])
        all_categories_names.append(list_book.string.strip())
    return all_categories_url, all_categories_names


def get_all_books_from_one_page():
    response = html_content(one_category_url)
    all_book_in_one_page = []
    list_books = response.find('ol', {'class': 'row'}).find_all('h3')
    for list_book in list_books:
        all_book_in_one_page.append(f"{domain}" + list_book.a["href"].strip('./'))

    return all_book_in_one_page

def get_books_data


get_all_books_from_one_page()
