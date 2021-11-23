'''
Provides a basic frontend
'''
#pylint: disable=W0614, W0401, C0103, R0903, E0401, W0120
import sys
from peewee import SqliteDatabase
from loguru import logger
import main

logger.remove()  # removing console output
logger.add("file_{time}.log")
logger.info("TEST MESSAGE FROM MENU")

def load_users():
    '''
    Loads user accounts from a file
    '''
    filename = input('Enter filename of user file: ')
    main.load_users(filename, user_collection)

def load_status_updates():
    '''
    Loads status updates from a file
    '''
    filename = input('Enter filename for status file: ')
    main.load_status_updates(filename, status_collection)

def add_user():
    '''
    Adds a new user into the database
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.add_user(user_id, email, user_name, user_last_name, user_collection):
        print("An error occurred while trying to add new user")
    else:
        print("User was successfully added")

def update_user():
    '''
    Updates information for an existing user
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    # if not main.update_user(user_id, email, user_name, user_last_name): --> FOR ASSIGNMENT
    if not main.update_user(user_id, email, user_name, user_last_name, user_collection):
        print("An error occurred while trying to update user")
    else:
        print("User was successfully updated")

def search_user():
    '''
    Searches a user in the database
    '''
    user_id = input('Enter user ID to search: ')
    result = main.search_user(user_id, user_collection)
    # if not result.name: --> FOR ASSIGNMENT
    if not result:
        print("ERROR: User does not exist")
    else:
        print(f"User ID: {result.user_id}")
        print(f"Email: {result.user_email}")
        print(f"Name: {result.user_name}")
        print(f"Last name: {result.user_last_name}")

def delete_user():
    '''
    Deletes user from the database
    '''
    user_id = input('User ID: ')
    if not main.delete_user(user_id, user_collection):
        print("An error occurred while trying to delete user")
    else:
        print("User was successfully deleted")

def save_users():
    '''
    Saves user database into a file
    '''
    filename = input('Enter filename for users file: ')
    main.save_users(filename, user_collection)

def add_status():
    '''
    Adds a new status into the database
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.add_status(user_id, status_id, status_text, status_collection):
        print("An error occurred while trying to add new status")
    else:
        print("New status was successfully added")

def update_status():
    '''
    Updates information for an existing status
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    #if not main.add_status(user_id, status_id, status_text, status_collection): --> FOR ASSIGNMENT
    if not main.update_status(status_id, user_id, status_text, status_collection):
        print("An error occurred while trying to update status")
    else:
        print("Status was successfully updated")

def search_status():
    '''
    Searches a status in the database
    '''
    status_id = input('Enter status ID to search: ')
    result = main.search_status(status_id, status_collection)
    if not result.user_id:
        print("ERROR: Status does not exist")
    else:
        print(f"User ID: {result.user_id}")
        print(f"Status ID: {result.status_id}")
        print(f"Status text: {result.status_text}")

def search_all_status_updates():
    '''
    Searches all status for a user in the database
    '''
    user_id = input('Enter user ID to search: ')
    result = main.search_all_status_updates(user_id, status_collection)
    print(f"A total {len(result)} status updates found for {user_id}")
    status = status_generator(result)
    while True:
        user_choice = input("Would you like to see the next update? (Y/N):").upper().strip()
        if user_choice == "Y":
            try:
                print(next(status))
            except StopIteration:
                print("INFO: You have reached the last update.")
                break
        elif user_choice == "N":
            break
        else:
            print("Invalid option")


def status_generator(collection_of_status):
    '''
    Generates individual status for a collection
    '''
    for status in collection_of_status:
        yield status.status_text


def filter_status_by_string():
    '''
    Searches all status matching a string
    '''
    phrase = input('Enter the string to search: ')
    result = main.filter_status_by_string(phrase, status_collection)
    for status in result:
        user_choice = input("Review the next status? (Y/N): ").upper().strip()
        if user_choice == "Y":
            print(status.status_text)
            user_choice_2 = input("Delete this status? (Y/N): ").upper().strip()
            if user_choice_2 == "Y":
                status.delete_instance()
                print("Status deleted!")
        elif user_choice == "N":
            break
        else:
            print("Invalid option")
    else:
        print("No match found.")

def flagged_status_updates():
    '''
    Print a list of all status updates matching a string
    '''
    phrase = input('Enter the string to search: ')
    result = main.filter_status_by_string(phrase, status_collection)
    list_of_status = [(status.status_id, status.status_text) for status in result]
    for status in list_of_status:
        print(status)
    else:
        print("No match found.")

def delete_status():
    '''
    Deletes status from the database
    '''
    status_id = input('Status ID: ')
    if not main.delete_status(status_id, status_collection):
        print("An error occurred while trying to delete status")
    else:
        print("Status was successfully deleted")

def save_status():
    '''
    Saves status database into a file
    '''
    filename = input('Enter filename for status file: ')
    main.save_status_updates(filename, status_collection)

def quit_program():
    '''
    Quits program
    '''
    sys.exit()

if __name__ == '__main__':
    database = SqliteDatabase('socialnetwork.db')
    database.connect()
    user_collection = main.init_user_collection(database)
    status_collection = main.init_status_collection(database)
    menu_options = {
        'A': load_users,
        'B': load_status_updates,
        'C': add_user,
        'D': update_user,
        'E': search_user,
        'F': delete_user,
        'G': save_users,
        'H': add_status,
        'I': update_status,
        'J': search_status,
        'K': search_all_status_updates,
        'L': filter_status_by_string,
        'M': flagged_status_updates,
        'N': delete_status,
        'O': save_status,
        'P': quit_program
    }
    while True:
        user_selection = input("""
                            A: Load user database
                            B: Load status database
                            C: Add user
                            D: Update user
                            E: Search user
                            F: Delete user
                            G: Save user database to file
                            H: Add status
                            I: Update status
                            J: Search status
                            K: Search all status updates
                            L: Search all status updates matching a string
                            M: Show all flagged status updates
                            N: Delete status
                            O: Save status database to file
                            P: Quit

                            Please enter your choice: """)
        if user_selection.upper() in menu_options:
            menu_options[user_selection.upper()]()
        else:
            print("Invalid option")
