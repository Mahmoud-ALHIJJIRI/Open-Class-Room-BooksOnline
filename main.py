import pprint
import functions
import print_menu
from functions_groupe import extracting_data_from_a_book


def main_menu():
    """
    Affiche le menu principale
    """
    print(print_menu.MENU)
    choice = input('Your choice : ')
    selection_available = ["1", "2", "3", "4", "5", "6"]

    while choice in selection_available:
        if choice == "1":
            extracting_data_from_a_book()
            exit()
        elif choice == "2":
            extracting_data_for_all_books_in_category()
            exit()
        elif choice == "3":
            extracting_data_for_all_books_in_site()
            exit()
        elif choice == "4":
            extracting_images_from_category()
            exit()
        elif choice == "5":
            extracting_all_images_from_the_site()
            exit()
        elif choice == "6":
            print("Good Bye")
            exit()

    while choice not in selection_available:
        print("Choose a number from the list")
        main_menu()


main_menu()