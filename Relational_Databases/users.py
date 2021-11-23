"""
Classes for user information for the
social network project
"""
# pylint: disable=R0903
# pylint: disable=C0301 (line-too-long)
# pylint: disable=E0401, W0150

from loguru import logger
import peewee
from socialnetwork_model import UsersTable


class UserCollection:
    """
    Contains a collection of Users objects
    """

    def __init__(self, database):
        self.database = database
        logger.debug("User Collection initialised")

    def add_user(self, user_id, email, user_name, user_last_name):
        """
        Adds a new user to the collection
        """
        try:
            self.database.connect(reuse_if_open=True)
            new_user = UsersTable.create(id=user_id, name=user_name, last_name=user_last_name, user_email=email)
            new_user.save()
            logger.info(f"New User added: ({user_id}, {email}, {user_name}, {user_last_name})")
            return True
        except peewee.IntegrityError:
            logger.warning(f"user_id:{user_id} entry could not be made.")
            return False
        finally:
            self.database.close()

    def modify_user(self, user_id, email, user_name, user_last_name):
        """
        Modifies an existing user
        """
        try:
            self.database.connect(reuse_if_open=True)
            modified_user = UsersTable.get(UsersTable.id == user_id)
            modified_user.user_email = email
            modified_user.name = user_name
            modified_user.last_name = user_last_name
            modified_user.save()
            logger.info(
                f"User modified - new_email:{email}, new_user_name:{user_name}, new_user_last_name: {user_last_name})")
            return True
        except peewee.DoesNotExist:
            logger.warning(f"user_id:{user_id} doesn't exist and cannot be modified.")
            return False
        finally:
            self.database.close()

    def delete_user(self, user_id):
        """
        Deletes an existing user
        """
        try:
            self.database.connect(reuse_if_open=True)
            user = UsersTable.get(UsersTable.id == user_id)
            user.delete_instance()
            logger.info(f"{user_id} deleted from database.")
            return True
        except peewee.DoesNotExist:
            logger.warning(f"user_id:{user_id} doesn't exist and cannot be deleted.")
            return False
        finally:
            self.database.close()

    def search_user(self, user_id):
        """
        Searches for user data
        """
        user = None
        try:
            self.database.connect(reuse_if_open=True)
            user = UsersTable.get(UsersTable.id == user_id)
            logger.info(f"{user_id} found in search database.")
        except peewee.DoesNotExist:
            logger.warning(f"user_id:{user_id} not found in the database.")
            user = None
        finally:
            self.database.close()
            return user
