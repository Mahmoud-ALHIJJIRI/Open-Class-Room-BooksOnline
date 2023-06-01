# Import required modules
import requests
from bs4 import BeautifulSoup
import csv
import os


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
    title = response.find('title').text.strip()
    price_including_tax = table[3].text
    price_excluding_tax = table[2].text
    number_available = table[5].text.split()[2].replace('(', '')
    div_product_description = response.find('div', {'id': 'product_description'})
    try:
        if div_product_description is not None:
            product_description = div_product_description.find_next_sibling().text
        else:
            product_description = ''
    except TypeError:
        product_description = ''

    category = response.find('ul', {'class': 'breadcrumb'}).find_all('a')[2].text.strip()
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


# Function to get all category names and URLs
def get_all_categories_names_and_url():
    # Get the HTML content of the domain URL
    response = html_content(domain)

    # Lists to store the category URLs and names
    all_categories_url = []
    all_categories_names = []

    # Find the list of categories in the HTML
    list_books = response.find('ul', {'class': 'nav nav-list'}).find('ul').find_all('li')

    # Iterate over each category and extract its URL and name
    for list_book in list_books:
        # Append the domain to the relative URL and add it to the URL list
        all_categories_url.append(f"{domain}" + list_book.a['href'])
        # Extract the text of the category name and add it to the name list
        all_categories_names.append(list_book.text.strip())

    # Return the lists of category URLs and names
    return all_categories_url, all_categories_names


# Function to get all page URLs for a category
def get_category_pages_urls(category_url):
    # List to store page URLs, starting with the initial category URL
    page_urls = [category_url]
    # Boolean variable to check if the next page exists
    next_page_exists = True

    # Continue the loop until there are no more next pages
    while next_page_exists:
        # Get the HTML content of the category URL
        response = html_content(category_url)

        # Find the next page link in the HTML
        next_page_link = response.find('li', class_='next')

        # Check if the next page link exists
        if next_page_link is None:
            next_page_exists = False
        else:
            # Construct the URL of the next page
            next_page_url = category_url.rsplit('/', 1)[0] + '/' + next_page_link.find('a')['href']

            # Append the next page URL to the list
            page_urls.append(next_page_url)

            # Update the category_url variable for the next iteration
            category_url = next_page_url

    # Return the list of page URLs
    return page_urls


# Function to get all books from all pages of a category
def get_all_books_from_all_pages(page_url):
    # List to store all book URLs from all pages
    all_book_in_all_pages = []

    # Iterate over each page URL in the category
    for list_book in get_category_pages_urls(page_url):
        # Get the HTML content of the page URL
        response = html_content(list_book)

        # Find all book elements in the HTML
        list_books = response.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})

        # Iterate over each book element and extract its URL
        for link in list_books:
            # Construct the full book URL and append it to the list
            all_book_in_all_pages.append(f"{domain}" + "catalogue/" + link.a["href"].strip('./'))

    # Return the list of all book URLs
    return all_book_in_all_pages


# Function to get all data for books from a single category
def get_all_data_from_one_category(category_url):
    # List to store all book data for a category
    all_books_data_one_category = []

    # Iterate over each book URL in the category
    for books_data in get_all_books_from_all_pages(category_url):
        # Get the book data using the one_book_data() functions
        book_data = one_book_data(books_data)

        # Append the book data to the list
        all_books_data_one_category.append(book_data)

        # Print the book data (optional, for demonstration)
        print(book_data)

    # Return the list of all book data for the category
    return all_books_data_one_category


def write_one_category_books_data_to_csv(category_url, selected_category):
    # Define the headers of the CSV file
    headers = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
               "number_available", "product_description", "category", "review_rating", "image_url"]

    # Open the CSV file for writing and write the headers as the first row
    with open(f"{selected_category}.csv", 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(headers)

        # Get the book URLs for the category
        book_urls = get_all_books_from_all_pages(category_url)

        # Iterate over the list of URLs and write the data for each book
        for url in book_urls:
            book_data = one_book_data(url)
            writer.writerow(book_data)


# Function to check and select a category
def check_category():
    # Get all category names from the website
    all_categories = get_all_categories_names_and_url()[1]

    # Print the available categories
    print(f"Categories: {all_categories}")

    # Loop until a valid category is selected or the user chooses to exit
    while True:
        # Prompt the user to choose a category or exit
        category = input("Choose one category (or write 'exit' to exit): ")

        # Check if the user chooses to exit
        if category.lower() == "exit":
            print("You chose to exit the program. Goodbye!")
            exit()

        # Check if the selected category is valid
        if category in all_categories:
            break

        # Print an error message and the available categories if the selection is invalid
        print("Error: Category not available")
        print(f"Choose from this list: {all_categories}")

    # Print the selected category and return it
    print(f"You have selected: {category}")
    return category


def create_new_folder():
    # Create a new folder
    folder_path = './All_Categories'
    os.makedirs(folder_path, exist_ok=True)


# Function to get all books data from all categories
def get_all_books_data():
    # Iterate over each category URL
    for all_category in get_all_categories_names_and_url()[0]:
        print(all_category)

        # Get the HTML content of the category URL
        response = html_content(all_category)

        # Extract the category name from the HTML
        category_name = response.find("div", {"class": "page-header action"}).find("h1").text

        # Print the number of books data for the category
        print(len(get_all_data_from_one_category(all_category)))

        # Write the books data for the category to a CSV file
        write_one_category_books_data_to_csv(all_category, category_name)

    # Return (optional, as the function doesn't have a specific return value)
    return
