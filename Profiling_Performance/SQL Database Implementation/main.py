# pylint: disable=E0401 (import-error)
# pylint: disable=C0114 (missing-module-docstring)
# pylint: disable=C0103

import csv
import users
import user_status
from peewee import chunked
from socialnetwork_model import UsersTable, StatusTable


def init_user_collection(database):
    """
    Creates and returns a new instance
    of UserCollection
    """
    return users.UserCollection(database)


def init_status_collection(database):
    """
    Creates and returns a new instance
    of UserStatusCollection
    """
    return user_status.UserStatusCollection(database)


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
    list_of_users = []
    with open(filename, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            for k, v in row.items():
                if k == "" or v == "":
                    return False
                user = {"id": row["USER_ID"],
                        "name": row["NAME"],
                        "last_name": row["LASTNAME"],
                        "user_email": row["EMAIL"]}
            list_of_users.append(user)
        with user_collection.database.transaction():
            UsersTable.insert_many(list_of_users).execute()
    return True


def save_users(filename, user_collection):
    """
    Saves all users in user_collection into
    a CSV file

    Requirements:
    - If there is an existing file, it will
    overwrite it.
    - Returns False if there are any errors
    (such an invalid filename).
    - Otherwise, it returns True.
    """
    with open(filename, mode='w') as csv_file:
        file_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        file_writer.writerow(['USER_ID', 'EMAIL', 'NAME', 'LASTNAME'])
        # Iterate through the collection of users
        for user in user_collection.database.values():
            file_writer.writerow([user.user_id, user.email, user.user_name, user.user_last_name])
    return True


def load_status_updates(filename, status_collection):
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
    list_of_status = []
    with open(filename, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            for k, v in row.items():
                if k == "" or v == "":
                    return False
                status = {"status_id": row["STATUS_ID"],
                          "id": row["USER_ID"],
                          "status_text": row["STATUS_TEXT"]}
            list_of_status.append(status)
        with status_collection.database.atomic():
            for batch in chunked(list_of_status, 100):
                StatusTable.insert_many(batch).execute()
    return True


def save_status_updates(filename, status_collection):
    """
    Saves all statuses in status_collection into
    a CSV file

    Requirements:
    - If there is an existing file, it will
    overwrite it.
    - Returns False if there are any errors
    (such an invalid filename).
    - Otherwise, it returns True.
    """
    with open(filename, mode='w') as csv_file:
        file_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        file_writer.writerow(['STATUS_ID', 'USER_ID', 'STATUS_TEXT'])
        # Iterate through the collection of user status
        for status in status_collection.database.values():
            file_writer.writerow([status.status_id, status.user_id, status.status_text])
    return True


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
    return user_collection.add_user(user_id, email, user_name, user_last_name)


def update_user(user_id, email, user_name, user_last_name, user_collection):
    """
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    """
    # Create an instance of Users for the updated user
    return user_collection.modify_user(user_id, email, user_name, user_last_name)


def delete_user(user_id, user_collection):
    """
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    """
    return user_collection.delete_user(user_id)


def search_user(user_id, user_collection):
    """
    Searches for a user in user_collection
    (which is an instance of UserCollection).

    Requirements:
    - If the user is found, returns the corresponding
    User instance.
    - Otherwise, it returns None.
    """
    return user_collection.search_user(user_id)


def add_status(user_id, status_id, status_text, status_collection):
    """
    Creates a new instance of UserStatus and stores it in user_collection
    (which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
    user_collection.add_status() returns False).
    - Otherwise, it returns True.
    """
    return status_collection.add_status(status_id, user_id, status_text)


def update_status(status_id, user_id, status_text, status_collection):
    """
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    """
    return status_collection.modify_status(status_id, user_id, status_text)


def delete_status(status_id, status_collection):
    """
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    """
    return status_collection.delete_status(status_id)


def search_status(status_id, status_collection):
    """
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    """
    return status_collection.search_status(status_id)
