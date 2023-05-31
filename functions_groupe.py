from pprint import pprint
import functions


def extracting_data_from_a_book():
    """Extract data from a book."""
    return pprint(functions.one_book_data(functions.url_book)), functions.write_book_data_to_csv(functions.url_book)


def extracting_data_for_books_in_one_category():
    names_categories = functions.get_all_categories_names_and_url()[1]
    url_categories = functions.get_all_categories_names_and_url()[0]
    selected_category = functions.check_category()
    index = names_categories.index(selected_category)
    selected_category_url = url_categories[index]
    functions.get_all_data_from_one_category(selected_category_url)
    functions.write_one_category_books_data_to_csv(selected_category_url, selected_category)
    return


"""def extracting_data_for_all_books_in_site():
"""

"""extracting_data_for_books_in_one_category()"""
