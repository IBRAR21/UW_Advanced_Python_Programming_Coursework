"""
Classes for status information for the
social network project
"""
# pylint: disable=R0903
# pylint: disable=R1705
# pylint: disable=C0115 (missing-class-docstring)
# pylint: disable=C0116 (missing-function-docstring)
# pylint: disable=C0301 (line-too-long)


from loguru import logger
import pymongo


class UserStatusCollection():
    def __init__(self, database):
        self.database = database
        logger.info("User Status Collection initialised")

    def add_status(self, status_id, user_id, status_text):
        if self.database.UserAccounts.find_one({"_id": user_id}):
            new_status = {"_id": status_id,
                          "user_id": user_id,
                          "status_text": status_text}
            try:
                self.database.StatusUpdates.insert_one(new_status)
                logger.info(f"New Status added: ({status_id}, {user_id}, {status_text})")
                return True
            except pymongo.errors.DuplicateKeyError:
                logger.warning(f"status_id:{status_id} already exited in the database. Another entry cannot be made.")
                return False
        else:
            logger.warning(f"user_id:{user_id} doesn't exist and the status cannot be added.")
            return False

    def modify_status(self, status_id, user_id, status_text):
        if self.database.StatusUpdates.find_one({"_id": status_id}):
            if self.database.UserAccounts.find_one({"_id": user_id}):
                modified_status = {"_id": status_id,
                                 "user_id": user_id,
                                 "status_text": status_text}
                self.database.StatusUpdates.update_one({"_id": status_id}, {"$set": modified_status})
                logger.info(f"Status modified - new_user_id:{user_id}, new_status_text:{status_text})")
                return True
            else:
                logger.warning(f"user_id:{user_id} doesn't exist and the status cannot be modified.")
                return False
        else:
            logger.warning(f"status_id:{status_id} doesn't exist and cannot be modified.")
            return False

    def delete_status(self, status_id):
        if self.database.StatusUpdates.find_one({"_id": status_id}):
            self.database.StatusUpdates.delete_one({"_id": status_id})
            logger.info(f"{status_id} deleted from database.]")
            return True
        else:
            logger.warning(f"status_id:{status_id} doesn't exist and cannot be deleted.")
            return False

    def search_status(self, status_id):
        if self.database.StatusUpdates.find_one({"_id": status_id}):
            logger.info(f"{status_id} found in search database.")
            return self.database.StatusUpdates.find_one({"_id": status_id})
        else:
            logger.warning(f"status_id:{status_id} not found in the database.")
            return False
