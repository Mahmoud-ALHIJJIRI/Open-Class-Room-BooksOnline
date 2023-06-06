# Import required modules
import os

import requests
from bs4 import BeautifulSoup

import functions

# Define the URL and domain name of the website
domain = 'http://books.toscrape.com/'


# Function to get the HTML content of a URL and parse it using BeautifulSoup
def html_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


# Function to extract and save images from a given link
def extract_images(link):
    # Print the provided link
    print(link)

    # Get the HTML content of the link
    response = html_content(link)

    # Find all image tags in the HTML
    images = response.find_all('img')

    # Iterate over each image
    for image in images:
        # Extract the name and link of the image
        name_image = image['alt'].replace(":", " ").replace("/", " ").replace("\"", " ").replace("*", " ")\
            .replace("?", " ").lstrip()
        link_image = f'{domain}/' + image['src'].lstrip('./')

        # Open a file and write the image content
        with open(name_image + '.jpg', 'wb') as file:
            img = requests.get(link_image)
            file.write(img.content)

        # Print the name and link of the written image
        print('Writing: ', name_image)
        print(link_image)


def extracting_image_from_1_category():
    names_categories = functions.get_all_categories_names_and_url()[1]
    urls_categories = functions.get_all_categories_names_and_url()[0]
    category = functions.check_category()
    index = [link_text for link_text in names_categories].index(category)
    category_url = urls_categories[index]
    try:
        os.mkdir(os.getcwd() + f"/images/")
        os.mkdir(os.getcwd() + f"/images/{category}")
    except TypeError:
        pass
    os.chdir(os.getcwd() + f"/images/{category}")
    for page_url in functions.get_category_pages_urls(category_url):
        extract_images(page_url)


# Function to extract all images from the website
def extracting_all_images_from_the_site():
    try:
        # Create a new directory to store the images
        os.mkdir(os.getcwd() + "/all-images")
    except TypeError:
        pass

    # Change the current working directory to the newly created directory
    os.chdir(os.getcwd() + "/all-images")

    # Get all category links
    links = functions.get_all_categories_names_and_url()[0]

    # Iterate over each category link
    for link in links:
        # Iterate over each page URL within the category
        for page_url in functions.get_all_books_from_all_pages(link):
            # Extract and save images from the page URL
            extract_images(page_url)
