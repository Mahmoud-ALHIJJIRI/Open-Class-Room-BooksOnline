import print_menu
import functions_groupe

print("er")


def main_menu():
    """
    Show Main Menu
    """
    print(print_menu.MENU)
    choice = input('Your choice : ')
    selection_available = ["1", "2", "3", "4", "5", "6"]

    while choice in selection_available:
        if choice == "1":
            functions_groupe.extracting_data_from_a_book()
            exit()
        elif choice == "2":
            functions_groupe.extracting_data_for_books_in_one_category()
            exit()
        elif choice == "3":
            print("In Progress")
            # extracting_data_for_all_books_in_site()
            exit()
        elif choice == "4":
            print("In Progress")
            # extracting_images_from_category()
            exit()
        elif choice == "5":
            print("In Progress")
            # extracting_all_images_from_the_site()
            exit()
        elif choice == "6":
            print("Good Bye")
            exit()

    while choice not in selection_available:
        print("Choose a number from the list")
        main_menu()


if __name__ == "__main__":
    main_menu()
