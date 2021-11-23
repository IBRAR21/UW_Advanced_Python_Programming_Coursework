"""
Classes for status information for the
social network project
"""
# pylint: disable=R0903
# pylint: disable=C0115 (missing-class-docstring)
# pylint: disable=C0116 (missing-function-docstring)
# pylint: disable=C0301 (line-too-long)
# pylint: disable=W0401, E0401, W0150, W0614


from loguru import logger
import peewee
from socialnetwork_model import *


class UserStatusCollection:
    def __init__(self, database):
        self.database = database
        logger.debug("User Status Collection initialised")

    def add_status(self, status_id, user_id, status_text):
        try:
            self.database.connect(reuse_if_open=True)
            new_status = StatusTable.create(status_id=status_id, id=user_id, status_text=status_text)
            new_status.save()
            logger.info(f"New Status added: ({status_id}, {user_id}, {status_text})")
            return True
        except peewee.IntegrityError:
            logger.warning(f"status_id:{status_id} could not be made.")
            return False
        finally:
            self.database.close()

    def modify_status(self, status_id, user_id, status_text):
        try:
            self.database.connect(reuse_if_open=True)
            StatusTable.get(id=user_id)
            modified_status = StatusTable.get(StatusTable.status_id == status_id)
            modified_status.status_text = status_text
            modified_status.save()
            logger.info(f" status_id: {status_id} modified -  new_status_text:{status_text})")
            return True
        except peewee.DoesNotExist:
            logger.warning(f"status_id:{status_id} or user_id:{id} doesn't exist and cannot be modified.")
            return False
        finally:
            self.database.close()

    def delete_status(self, status_id):
        try:
            self.database.connect(reuse_if_open=True)
            status = StatusTable.get(StatusTable.status_id == status_id)
            status.delete_instance()
            logger.info(f"{status_id} deleted from database.")
            return True
        except peewee.DoesNotExist:
            logger.warning(f"status_id:{status_id} doesn't exist and cannot be deleted.")
            return False
        finally:
            self.database.close()

    def search_status(self, status_id):

        status = None
        try:
            self.database.connect(reuse_if_open=True)
            status = StatusTable.get(StatusTable.status_id == status_id)
            logger.info(f"{status_id} found in search database.")
        except peewee.DoesNotExist:
            logger.warning(f"status_id:{status_id} not found in the database.")
            status = None
        finally:
            self.database.close()
            return status
