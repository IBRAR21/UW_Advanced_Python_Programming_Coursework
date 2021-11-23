# pylint: disable=E0401 (import-error)
# pylint: disable=C0114 (missing-module-docstring)
# pylint: disable=C0103

import csv
import users
import user_status
import peewee
from loguru import logger


def load_users(filename, user_collection):
    """
    Opens a CSV file with user data and
    adds it to an existing instance of
    UserCollection

    Requirements:
    - If a user_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    """
    try:
        with open(filename, newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                for k, v in row.items():
                    if k == "" or v == "":
                        return False
                try:
                    user_collection.insert(user_id = row['USER_ID'],
                                            user_name = row['NAME'],
                                            user_last_name = row['LASTNAME'],
                                            email = row['EMAIL'])
                except peewee.IntegrityError:
                    logger.warning(f"user_id:{user_id} already existed. Duplicate entry cannot be made.")
        return True
    except FileNotFoundError:
        logger.debug(f"File not found.")
        return False


def load_status_updates(filename, user_collection, status_collection):
    """
    Opens a CSV file with status data and
    adds it to an existing instance of
    UserStatusCollection

    Requirements:
    - If a status_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    """
    try:
        with open(filename, newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            add_status = load_status_closure(user_collection, status_collection)
            return add_status(reader)
    except FileNotFoundError:
        logger.debug(f"File not found.")
        return False

def load_status_closure(user_collection, status_collection):

    list_of_users = []
    def inner_function(reader):
        for row in reader:
            for k, v in row.items():
                if k == '' or v == '':
                    return False
            user_id = row['USER_ID']
            existing_user = False

            if user_id in list_of_users:
                existing_user = True
            else:
                if user_collection.find_one(user_id = row['USER_ID']):
                    list_of_users.append(user_id)
                    existing_user = True
            if existing_user:
                try:
                    status_collection.insert(status_id = row['STATUS_ID'],
                                             user_id = row['USER_ID'],
                                             status_text = row['STATUS_TEXT'])
                except peewee.IntegrityError:
                    logger.warning(f"status_id:{row['STATUS_ID']} already existed. Duplicate entry cannot be made.")
            else:
                logger.warning(f"user_id:{row['USER_ID']} doesnot exist. Entry cannot be made.")
        return True
    return inner_function


def add_user(user_id, email, user_name, user_last_name, user_collection):
    """
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
    user_collection.add_user() returns False).
    - Otherwise, it returns True.
    """
    return users.add_user(user_id, email, user_name, user_last_name, user_collection)


def update_user(user_id, email, user_name, user_last_name, user_collection):
    """
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    """
    # Create an instance of Users for the updated user
    return users.modify_user(user_id, email, user_name, user_last_name, user_collection)


def delete_user(user_id, user_collection, status_collection):
    """
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    """
    return users.delete_user(user_id, user_collection, status_collection)


def search_user(user_id, user_collection):
    """
    Searches for a user in user_collection
    (which is an instance of UserCollection).

    Requirements:
    - If the user is found, returns the corresponding
    User instance.
    - Otherwise, it returns None.
    """
    return users.search_user(user_id, user_collection)


def add_status(status_id, user_id, status_text, user_collection, status_collection):
    """
    Creates a new instance of UserStatus and stores it in user_collection
    (which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
    user_collection.add_status() returns False).
    - Otherwise, it returns True.
    """
    return user_status.add_status(status_id, user_id, status_text, user_collection, status_collection)


def update_status(status_id, user_id, status_text, user_collection, status_collection):
    """
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    """
    return user_status.modify_status(status_id, user_id, status_text, user_collection, status_collection)


def delete_status(status_id, status_collection):
    """
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    """
    return user_status.delete_status(status_id, status_collection)


def search_status(status_id, status_collection):
    """
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    """
    return user_status.search_status(status_id, status_collection)
