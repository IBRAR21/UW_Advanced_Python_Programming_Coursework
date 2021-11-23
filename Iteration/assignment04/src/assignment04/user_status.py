'''
Classes for status information for the
social network project
'''
#pylint: disable=E0602, E0401, W0401, C0301
from loguru import logger
from socialnetwork_model import *
logger.info("TEST MESSAGE FROM STATUS")

class UserStatusCollection():
    '''
    Contains a collection of status objects
    '''
    def __init__(self, social_database):
        '''
        Initializes the database
        '''
        self.database = social_database
        logger.info("New status collection instance created")

    def add_status(self, user_id, status_id, status_text):
        '''
        Adds a new status to the database
        '''
        with self.database.transaction():
            try:
                new_status = StatusTable.create(
                    status_id=status_id,
                    user_id=user_id,
                    status_text=status_text
                )
                new_status.save()
                return True
            except IntegrityError:
                return False

    def modify_status(self, status_id, user_id, status_text):
        '''
        Modifies an existing status
        '''
        with self.database.transaction():
            try:
                modify_target = StatusTable.get(StatusTable.status_id == status_id)
                modify_target.user_id = user_id
                modify_target.status_text = status_text
                modify_target.save()
                return True
            except DoesNotExist:
                return False

    def delete_status(self, status_id):
        '''
        Deletes an existing status
        '''
        with self.database.transaction():
            try:
                delete_target = StatusTable.get(StatusTable.status_id == status_id)
                delete_target.delete_instance()
                return True
            except DoesNotExist:
                return False

    def search_status(self, status_id):
        '''
        Searches and returns the information from an existing status
        '''
        with self.database.transaction():
            try:
                target = StatusTable.get(StatusTable.status_id == status_id)
            except DoesNotExist:
                target = None
            return target

    def search_all_status_updates(self, user_id):
        '''
        Searches and returns the status for an existing user_id
        '''
        with self.database.transaction():
            try:
                query = StatusTable.select(StatusTable.status_text).where(StatusTable.user_id == user_id)
                logger.info(f"Status found for {user_id} in search database.")
            except DoesNotExist:
                query = None
                logger.info(f"Status not found for {user_id} in search database.")
            return query

    def filter_status_by_string(self, phrase):
        '''
        Searches and returns all status that contain a phrase
        '''
        with self.database.transaction():
            try:
                query = StatusTable.select().where(StatusTable.status_text.contains(phrase)).iterator()
                logger.info(f"Status found for {phrase} in search database.")
            except DoesNotExist:
                query = None
                logger.info(f"Status not found for {phrase} in search database.")
            return query
