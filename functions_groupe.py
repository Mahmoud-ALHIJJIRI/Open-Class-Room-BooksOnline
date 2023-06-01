from pprint import pprint
import functions
import image_functions

domain = 'http://books.toscrape.com/'


def extracting_data_from_a_book():
    """Extract data from a book."""
    return pprint(functions.one_book_data(functions.url_book)), functions.write_book_data_to_csv(functions.url_book)


# Function to extract data for books in one selected category
def extracting_data_for_books_in_one_category():
    # Get all category names and URLs
    names_categories = functions.get_all_categories_names_and_url()[1]
    url_categories = functions.get_all_categories_names_and_url()[0]

    # Prompt the user to select a category
    selected_category = functions.check_category()

    # Get the index of the selected category
    index = names_categories.index(selected_category)

    # Get the URL of the selected category
    selected_category_url = url_categories[index]

    # Get all data for books in the selected category
    functions.get_all_data_from_one_category(selected_category_url)

    # Write the books data for the selected category to a CSV file
    functions.write_one_category_books_data_to_csv(selected_category_url, selected_category)

    # Return (optional, as the function doesn't have a specific return value)
    return


# Function to extract data for all books on the website
def extracting_data_for_all_books_onsite():
    # Get all books data from all categories
    functions.get_all_books_data()

    # Return (optional, as the function doesn't have a specific return value)
    return


def extracting_image_from_one_category():
    image_functions.extracting_image_from_1_category()
    return


def extracting_image_from_all_site():
    image_functions.extracting_all_images_from_the_site()
    return
