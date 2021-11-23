"""
Classes for user information for the
social network project
"""
# pylint: disable=R0903
# pylint: disable=C0301 (line-too-long)
# pylint: disable=E0401, W0150

from loguru import logger
import peewee

def check_user_constraints(user_id, email, user_name, user_last_name):
    '''
    Checks that inputs meet constraints
    '''
    if len(user_id) > 30:
        logger.debug(f"user_id:{user_id} entry cannot be longer than 30 characters.")
        return False
    if len(user_name) > 30:
        logger.debug(f"user_name:{user_name} entry cannot be longer than 30 characters.")
        return False
    if len(user_last_name) > 100:
        logger.debug(f"user_last_name:{user_last_name} entry cannot be longer than 100 characters.")
        return False
    if len(email) == 0:
        logger.debug(f"email entry cannot be blank.")
        return False
    return True



def add_user(user_id, email, user_name, user_last_name, user_collection):
    """
    Adds a new user to the collection
    """
    if check_user_constraints(user_id, email, user_name, user_last_name) is False:
        return False
    else:
        try:
            user_collection.insert(user_id=user_id,
                                   user_name=user_name,
                                   user_last_name=user_last_name,
                                   email=email)
            logger.info(f"New User added: ({user_id}, {email}, {user_name}, {user_last_name})")
            return True
        except peewee.IntegrityError:
            logger.warning(f"user_id:{user_id} already existed. Duplicate entry cannot be made.")
            return False

def modify_user(user_id, email, user_name, user_last_name, user_collection):
    """
        Modifies an existing user
        """
    if check_user_constraints(user_id, email, user_name, user_last_name) is False:
        return False
    else:
        if user_collection.find_one(user_id = user_id):
            user_collection.update(user_id=user_id,
                                   user_name=user_name,
                                   user_last_name=user_last_name,
                                   email=email,
                                   columns=['user_id'])
            logger.info(
                        f"User {user_id} modified - new_email:{email}, new_user_name:{user_name}, new_user_last_name: {user_last_name})")
            return True
        else:
            logger.warning(f"user_id:{user_id} doesn't exist and cannot be modified.")
            return False


def delete_user(user_id, user_collection, status_collection):
    """
    Deletes an existing user
    """
    if user_collection.find_one(user_id = user_id):
        status_collection.delete(user_id = user_id)
        user_collection.delete(user_id = user_id)
        logger.info(f"{user_id} deleted from database.")
        return True
    else:
        logger.warning(f"user_id:{user_id} doesn't exist and cannot be deleted.")
        return False

def search_user(user_id, user_collection):
    """
        Searches for user data
    """
    if user_collection.find_one(user_id = user_id):
        user = user_collection.find_one(user_id = user_id)
        logger.info(f"{user_id} found in search database.")
        return user
    else:
        logger.warning(f"user_id:{user_id} not found in the database.")
        return None

