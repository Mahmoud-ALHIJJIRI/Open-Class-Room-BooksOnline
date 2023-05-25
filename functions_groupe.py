from pprint import pprint
import functions


def extracting_data_from_a_book():
    """Extract data from a book."""
    return pprint(functions.one_book_data(functions.url_book)), functions.write_book_data_to_csv(functions.url_book)


def extracting_data_for_books_in_one_category():
    functions.check_category()
    return


extracting_data_for_books_in_one_category()
