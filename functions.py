# Import required modules
import requests
from bs4 import BeautifulSoup
import csv

import functions_groupe

# Define the URL and domain name of the website
url_book = 'http://books.toscrape.com/catalogue/rework_212/index.html'
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
        all_categories_names.append(list_book.text.strip())
    return all_categories_url, all_categories_names


def get_category_pages_urls(category_url):
    page_urls = [category_url]  # List to store page URLs
    next_page_exists = True
    while next_page_exists:
        response = html_content(category_url)
        next_page_link = response.find('li', class_='next')
        if next_page_link is None:
            next_page_exists = False
        else:
            next_page_url = category_url.replace('index.html', '') + next_page_link.find('a')['href']
            page_urls.append(next_page_url)
            category_url = next_page_url  # Update the current_page_url variable

    return page_urls


def get_all_books_from_all_pages(page_url):
    all_book_in_all_pages = []

    for list_book in get_category_pages_urls(page_url):
        response = html_content(page_url)
        list_books = response.find('ol', {'class': 'row'}).find_all('h3')
        for link in list_books:
            all_book_in_all_pages.append(f"{domain}" + "catalogue/" + link.a["href"].strip('./'))
    return all_book_in_all_pages


def get_all_data_from_one_category(category_url):
    all_books_data_one_category = []

    for books_data in get_all_books_from_all_pages(category_url):
        all_books_data_one_category.append(one_book_data(books_data))
        print(one_book_data(books_data))
    return all_books_data_one_category


def write_one_category_books_data_to_csv(category_url):
    # Define the headers of the CSV file
    headers = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
               "number_available", "product_description", "category", "review_rating", "image_url"]

    # Open the CSV file for writing and write the headers as the first row
    with open("selected_category.csv", 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(headers)

        # Get the book URLs for the category
        book_urls = get_all_books_from_all_pages(category_url)

        # Iterate over the list of URLs and write the data for each book
        for url in book_urls:
            book_data = one_book_data(url)
            writer.writerow(book_data)


def check_category():
    all_categories = get_all_categories_names_and_url()[1]
    print(f"Categories: {all_categories}")
    while True:
        category = input("Choose one category (or write 'exit' to exit): ")
        if category.lower() == "exit":
            print("You chose to exit the program. Goodbye!")
            exit()
        if category in all_categories:
            break
        print("Error: Category not available")
        print(f"Choose from this list: {all_categories}")
    print(f"You have selected: {category}")
    return category


"""def get_all_books_url(site, categories_url=None):
    all_books_url = []
    for all_url in all_books_url:
        all_books_url.append(get_all_categories_names_and_url()[0])"""


current_page_url = 'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html'
print(get_category_pages_urls(current_page_url))
