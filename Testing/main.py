import users
import user_status
import csv

def init_user_collection():
    '''
    Creates and returns a new instance 
    of UserCollection
    '''
    return users.UserCollection()

def init_status_collection():
    '''
    Creates and returns a new instance
    of UserStatusCollection
    '''
    return user_status.UserStatusCollection()

def load_users(filename, user_collection):
    '''
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
    '''
    with open(filename, newline= "") as user_file:
        data = csv.DictReader(user_file)
        for line in data:
            user_collection.add_user(line["USER_ID"], line["EMAIL"], line["NAME"], line["LASTNAME"])
    return True

def save_users(filename, user_collection):
    '''
    Saves all users in user_collection into
    a CSV file

    Requirements:
    - If there is an existing file, it will
    overwrite it.
    - Returns False if there are any errors
    (such an invalid filename).
    - Otherwise, it returns True.
    '''
    with open(filename, mode= "w") as new_user_file:
        new_data = csv.writer(new_user_file, delimiter=",", quotechar="\"", quoting=csv.QUOTE_MINIMAL)
        new_data.writerow(["USER_ID","EMAIL","NAME","LASTNAME"])
        for row in user_collection.database.values():
            new_data.writerow([row.user_id, row.email, row.user_name, row.user_last_name])
        return True


def load_status_updates(filename, status_collection):
    '''
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
    '''
    with open(filename, newline="") as status_file:
        data = csv.DictReader(status_file)
        for line in data:
            status_collection.add_status(line["STATUS_ID"], line["USER_ID"], line["STATUS_TEXT"])
    return True

def save_status_updates(filename, status_collection):
    '''
    Saves all statuses in status_collection into
    a CSV file

    Requirements:
    - If there is an existing file, it will
    overwrite it.
    - Returns False if there are any errors
    (such an invalid filename).
    - Otherwise, it returns True.
    '''
    with open(filename, mode= "w") as new_status_file:
        new_data = csv.writer(new_status_file, delimiter=",", quotechar="\"", quoting=csv.QUOTE_MINIMAL)
        new_data.writerow(["STATUS_ID","USER_ID","STATUS_TEXT"])
        for row in status_collection.database.values():
            new_data.writerow([row.status_id, row.user_id, row.status_text])
        return True

def add_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
    user_collection.add_user() returns False).
    - Otherwise, it returns True.
    '''
    return user_collection.add_user(user_id, email, user_name, user_last_name)

def update_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    return user_collection.modify_user(user_id, email, user_name, user_last_name)

def delete_user(user_id, user_collection):
    '''
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    '''
    return user_collection.delete_user(user_id)

def search_user(user_id, user_collection):
    '''
    Searches for a user in user_collection
    (which is an instance of UserCollection).

    Requirements:
    - If the user is found, returns the corresponding
    User instance.
    - Otherwise, it returns None.
    '''
    return user_collection.search_user(user_id)

def add_status(user_id, status_id, status_text, status_collection):
    '''
    Creates a new instance of UserStatus and stores it in user_collection
    (which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
    user_collection.add_status() returns False).
    - Otherwise, it returns True.
    '''
    return status_collection.add_status(user_id, status_id, status_text)

def update_status(status_id, user_id, status_text, status_collection):
    '''
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    return status_collection.modify_status(status_id, user_id, status_text)

def delete_status(status_id, status_collection):
    '''
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    '''
    return status_collection.delete_status(status_id)

def search_status(status_id, status_collection):
    '''
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    '''
    return status_collection.search_status(status_id)