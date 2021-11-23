"""
Classes for user information for the
social network project
"""
# pylint: disable=R0903
# pylint: disable=R1705
# pylint: disable=C0301 (line-too-long)

from loguru import logger
import pymongo


class UserCollection():
    """
    Contains a collection of Users objects
    """

    def __init__(self, database):
        self.database = database
        logger.info("User Collection initialised")

    def add_user(self, user_id, email, user_name, user_last_name):
        """
        Adds a new user to the collection
        """
        new_user = {"_id": user_id,
                    "email": email,
                    "user_name": user_name,
                    "user_last_name": user_last_name}
        try:
            self.database.UserAccounts.insert_one(new_user)
            logger.info(f"New User added: ({user_id}, {email}, {user_name}, {user_last_name})")
            return True
        except pymongo.errors.DuplicateKeyError:
            logger.warning(f"user_id:{user_id} already exited in the database. Another entry cannot be made.")
            return False

    def modify_user(self, user_id, email, user_name, user_last_name):
        """
        Modifies an existing user
        """
        if self.database.UserAccounts.find_one({"_id": user_id}):
            modified_user = {"_id": user_id,
                             "email": email,
                             "user_name": user_name,
                             "user_last_name": user_last_name}
            self.database.UserAccounts.update_one({"_id": user_id}, {"$set": modified_user})
            logger.info(
                f"User modified - new_email:{email}, new_user_name:{user_name}, new_user_last_name: {user_last_name})")
            return True
        else:
            logger.warning(f"user_id:{user_id} doesn't exist and cannot be modified.")
            return False

    def delete_user(self, user_id):
        """
        Deletes an existing user
        """
        if self.database.UserAccounts.find_one({"_id": user_id}):
            self.database.UserAccounts.delete_one({"_id": user_id})
            self.database.StatusUpdates.delete_many({"user_id": user_id})
            logger.info(f"{user_id} deleted from database.]")
            return True
        else:
            logger.warning(f"user_id:{user_id} doesn't exist and cannot be deleted.")
            return False

    def search_user(self, user_id):
        """
        Searches for user data
        """
        if self.database.UserAccounts.find_one({"_id": user_id}):
            logger.info(f"{user_id} found in search database.")
            return self.database.UserAccounts.find_one({"_id": user_id})
        else:
            logger.warning(f"user_id:{user_id} not found in the database.")
            return False
