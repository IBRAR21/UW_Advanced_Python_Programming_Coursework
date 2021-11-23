# pylint: disable=E0401 (import-error)
# pylint: disable=C0114 (missing-module-docstring)

import csv
import users
import user_status
from loguru import logger
import pymongo
import pandas as pd
import multiprocessing
from multiprocessing import Process
import mongoDBconnection as DB_con


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


def load_users(filename):
    """
    Opens a CSV file with user data and
    adds it to mongoDBdatabase

    Requirements:
    - If a user_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    """
    try:
        chunk_collection = get_chunk_list(filename)
        import_csv_in_chunks(chunk_collection, user_worker)
        return True
    except Exception as e:
        logger.exception(e)
        return False


def load_status_updates(filename):
    """
    Opens a CSV file with status data and
    adds it to the mongoDBdatabase

    Requirements:
    - If a status_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    """
    try:
        chunk_collection = get_chunk_list(filename)
        import_csv_in_chunks(chunk_collection, status_worker)
        return True
    except Exception as e:
        logger.warning(e)
        return False


def get_chunk_list(filename):
    try:
        #file = open(filename)
        #reader = csv.reader(file)
        #size = int(len(list(reader)) / multiprocessing.cpu_count())
        #size = int(len(list(reader)) / 2)

        chunk_list = pd.read_csv(filename, chunksize= 100000, iterator=True)
        return chunk_list
    except FileNotFoundError:
        logger.warning(f"File: {filename} not found.")
        raise FileNotFoundError


def import_csv_in_chunks(list_of_chunks, worker_function):
    processes = []
    for chunk in list_of_chunks:
        process = Process(target=worker_function, args=(chunk,))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()


def user_worker(chunk):
    mongo = DB_con.MongoDBConnection()
    with mongo:
        database = mongo.connection.SocialNetwork

        list_of_users = []
        for index, row in chunk.iterrows():
            for item in row:
                if item != "":
                    user = {"_id": row["USER_ID"],
                            "email": row["EMAIL"],
                            "user_name": row["NAME"],
                            "user_last_name": row["LASTNAME"]}
            list_of_users.append(user)
        try:
            database.UserAccounts.insert_many(list_of_users, ordered=False)
        except pymongo.errors.BulkWriteError as e:
            logger.warning(e.details)


def status_worker(chunk):
    mongo = DB_con.MongoDBConnection()
    with mongo:
        database = mongo.connection.SocialNetwork

        list_of_status = []
        for index, row in chunk.iterrows():
            for item in row:
                if item != "":
                    status = {"_id": row['STATUS_ID'],
                              "user_id": row['USER_ID'],
                              "status_text": row['STATUS_TEXT']}
            list_of_status.append(status)
        try:
            database.StatusUpdates.insert_many(list_of_status, ordered=False)
        except pymongo.errors.BulkWriteError as e:
            logger.warning(e.details)
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
