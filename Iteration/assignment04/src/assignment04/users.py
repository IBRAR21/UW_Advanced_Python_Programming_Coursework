'''
Classes for user information for the
social network project
'''
# pylint: disable=R0903
#pylint: disable=E0602, E0401, W0401
from loguru import logger
from socialnetwork_model import *

class UserCollection():
    '''
    Contains a collection of Users objects
    '''
    def __init__(self, social_database):
        self.database = social_database
        logger.info("New instance of UserCollection created")

    def add_user(self, user_id, user_email, user_name, user_last_name):
        '''
        Adds a new user to the collection
        '''
        with self.database.transaction():
            try:
                new_user = UsersTable.create(
                    user_id=user_id,
                    user_name=user_name,
                    user_last_name=user_last_name,
                    user_email=user_email
                )
                new_user.save()
                return True
            except IntegrityError:
                return False

    def modify_user(self, user_id, email, user_name, user_last_name):
        '''
        Modifies an existing user
        '''
        with self.database.transaction():
            try:
                modify_target = UsersTable.get(UsersTable.user_id == user_id)
                modify_target.user_name = user_name
                modify_target.user_last_name = user_last_name
                modify_target.user_email = email
                modify_target.save()
                return True
            except DoesNotExist:
                return False

    def delete_user(self, user_id):
        '''
        Deletes an existing user
        '''
        with self.database.transaction():
            try:
                delete_target = UsersTable.get(UsersTable.user_id == user_id)
                delete_target.delete_instance()
                return True
            except DoesNotExist:
                return False

    def search_user(self, user_id):
        '''
        Searches for user data
        '''
        with self.database.transaction():
            try:
                target = UsersTable.get(UsersTable.user_id == user_id)
            except DoesNotExist:
                target = None
            return target
