"""
Provides a basic frontend
"""
# pylint: disable=E0401 (import-error)
# pylint: disable=W0601 (global-variable-undefined)
# pylint: disable=C0103 (invalid-name)
# pylint: disable=C0116 (missing-function-docstring)
# pylint: disable=W0401, W0611, W0614, W0703, W0621

import sys
import os
from contextlib import contextmanager
import main
from peewee import *
from loguru import logger
import socialnetwork_model as snm
from playhouse.dataset import DataSet


logger.remove()  # removing console output
logger.add("log_{time:MM-DD-YYYY}.log", rotation="00:00")

file = 'socialnetwork.db'
        # if os.path.exists(file):
        #    os.remove(file)

@contextmanager
def dataset_connection(connection_type):
    '''
        Context manager for database connection
    '''
    database = DataSet(connection_type)
    try:
        logger.debug("Database opened")
        yield database

    except Exception as e:
        logger.debug(f'Error: {e}')
        if not connection_type:
            raise e

    finally:
        database.close()
        logger.debug("Database closed")


def load_users():
    """
    Loads user accounts from a file
    """
    filename = input('Enter filename of user file: ')
    if not main.load_users(filename, user_collection):
        print("An error occurred while trying to load users")
    else:
        print("Users loaded successfully!")


def load_status_updates():
    """
    Loads status updates from a file
    """
    filename = input('Enter filename for status file: ')
    if not main.load_status_updates(filename, user_collection, status_collection):
        print("An error occurred while trying to load status updates")
    else:
        print("Status updates loaded successfully!")


def add_user():
    """
    Adds a new user into the database
    """
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.add_user(user_id, email, user_name, user_last_name, user_collection):
        print("An error occurred while trying to add new user")
    else:
        print("User was successfully added")


def update_user():
    """
    Updates information for an existing user
    """
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.update_user(user_id, email, user_name, user_last_name, user_collection):
        print("An error occurred while trying to update user")
    else:
        print("User was successfully updated")


def search_user():
    """
    Searches a user in the database
    """
    user_id = input('Enter user ID to search: ')
    result = main.search_user(user_id, user_collection)
    if result is None:
        print("ERROR: User does not exist")
    else:
        print(f"User ID: {result['user_id']}")
        print(f"Email: {result['email']}")
        print(f"Name: {result['user_name']}")
        print(f"Last name: {result['user_last_name']}")


def delete_user():
    """
    Deletes user from the database
    """
    user_id = input('User ID: ')
    if not main.delete_user(user_id, user_collection, status_collection):
        print("An error occurred while trying to delete user")
    else:
        print("User was successfully deleted")


def add_status():
    """
    Adds a new status into the database
    """
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.add_status(status_id, user_id, status_text, user_collection, status_collection):
        print("An error occurred while trying to add new status")
    else:
        print("New status was successfully added")


def update_status():
    """
    Updates information for an existing status
    """
    status_id = input('Status ID: ')
    user_id = input('User ID: ')
    status_text = input('Status text: ')
    if not main.update_status(status_id, user_id, status_text, user_collection, status_collection):
        print("An error occurred while trying to update status")
    else:
        print("Status was successfully updated")


def search_status():
    """
    Searches a status in the database
    """
    status_id = input('Enter status ID to search: ')
    result = main.search_status(status_id, status_collection)
    if result is None:
        print("ERROR: Status does not exist")
    else:
        print(f"Status ID: {result['status_id']}")
        print(f"User ID: {result['user_id']}")
        print(f"Status text: {result['status_text']}")


def delete_status():
    """
    Deletes status from the database
    """
    status_id = input('Status ID: ')
    if not main.delete_status(status_id, status_collection):
        print("An error occurred while trying to delete status")
    else:
        print("Status was successfully deleted")


def add_image():
    """
    Adds a new image into the database
    """
    user_id = input('User ID: ')
    tags = input('Image Tags: ')
    if not main.add_image(user_id, tags, user_collection, image_collection):
        print("An error occurred while trying to add new image")
    else:
        print("New image was successfully added")


def list_of_user_images():
    """
    Adds a new image into the database
    """
    user_id = input('User ID: ')
    list_of_images = main.list_of_user_images(user_id)
    if list_of_images is None:
        print("No image found.")
    else:
        print(f"Following images found for user {user_id}:")
        for image in list_of_images:
            print(image)


def reconcile_images():
    """
    Adds a new image into the database
    """
    user_id = input('User ID: ')
    result = main.reconcile_images(user_id, user_collection, image_collection)
    if result is None:
        print("An error occurred while trying to reconcile status")
    else:
        if not result[0] and not result[1]:
            print("No differences found between images on drive and database")
        if result[0]:
            print(f"Following images were unique on database for user {user_id}:")
            for image in result[0]:
                print(image)
        if result[1]:
            print(f"Following images were unique on drive for user {user_id}:")
            for image in result[1]:
                print(image)


def quit_program():
    """
    Quits program
    """
    drop = input("Drop database? [Y/N]: ")
    if drop.lower() == 'y':
        if os.path.exists(file):
            os.remove(file)
    sys.exit()


if __name__ == "__main__":
    logger.debug(f"__name__:{__name__}")
    with logger.catch():
        connection_type = 'sqlite:///' + file
        with dataset_connection(connection_type) as db:
            user_collection, status_collection, image_collection = snm.create_tables(db)
            menu_options = {
            'A': load_users,
            'B': load_status_updates,
            'C': add_user,
            'D': update_user,
            'E': search_user,
            'F': delete_user,
            'G': add_status,
            'H': update_status,
            'I': search_status,
            'J': delete_status,
            'K': add_image,
            'L': list_of_user_images,
            'M': reconcile_images,
            'N': quit_program
            }
            while True:
                user_selection = input("""
                A: Load user database from csv file
                B: Load status database from csv file
                C: Add user
                D: Update user
                E: Search user
                F: Delete user
                G: Add status
                H: Update status
                I: Search status
                J: Delete status
                K: Add image
                L: List user images
                M: Reconcile user images
                N: Quit

                Please enter your choice: """).strip().upper()
                if user_selection in menu_options:
                    menu_options[user_selection]()
                else:
                    print("Invalid option")
