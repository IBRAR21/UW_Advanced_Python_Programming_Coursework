"""
Classes for status information for the
social network project
"""
# pylint: disable=R0903
# pylint: disable=C0115 (missing-class-docstring)
# pylint: disable=C0116 (missing-function-docstring)
# pylint: disable=C0301 (line-too-long)
# pylint: disable=W0401, E0401, W0150, W0614, R1705, W1309


from loguru import logger
import peewee


def check_status_constraints(status_id, user_id, status_text, user_collection):
    '''
    Checks status constraints
    '''
    if user_collection.find_one(user_id = user_id):
        if len(status_id) == 0:
            logger.debug(f"status_id entry cannot be blank.")
            return False
        if len(status_text) == 0:
            logger.debug(f"status_text entry cannot be blank.")
            return False
        return True
    else:
        logger.debug(f"user_id:{user_id} doesn't exist and status cannot be added.")
        return False



def add_status(status_id, user_id, status_text, user_collection, status_collection):
    if check_status_constraints(status_id, user_id, status_text, user_collection) is False:
        return False
    else:
        try:
            status_collection.insert(status_id=status_id,
                                     user_id=user_id,
                                     status_text=status_text)
            logger.info(f"New Status added: ({status_id}, {user_id}, {status_text})")
            return True
        except peewee.IntegrityError:
            logger.warning(f"status_id:{status_id} already existed. Duplicate entry cannot be made.")
            return False


def modify_status(status_id, user_id, status_text, user_collection, status_collection):
    if check_status_constraints(status_id, user_id, status_text, user_collection) is False:
        return False
    else:
        if  status_collection.find_one(status_id = status_id):
            status_collection.update(status_id = status_id,
                                     user_id = user_id,
                                     status_text = status_text,
                                   columns=['status_id'])
            logger.info(f" status_id: {status_id} modified -  new_status_text:{status_text})")
            return True
        else:
            logger.warning(f"status_id:{status_id} doesn't exist and cannot be modified.")
            return False

def delete_status(status_id, status_collection):
    if status_collection.find_one(status_id = status_id):
        status_collection.delete(status_id = status_id)
        logger.info(f"{status_id} deleted from database.")
        return True
    else:
        logger.warning(f"status_id:{status_id} doesn't exist and cannot be deleted.")
        return False

def search_status(status_id, status_collection):
    if status_collection.find_one(status_id = status_id):
        status = status_collection.find_one(status_id = status_id)
        logger.info(f"{status_id} found in search database.")
        return status
    else:
        logger.warning(f"status_id:{status_id} not found in the database.")
        return None
