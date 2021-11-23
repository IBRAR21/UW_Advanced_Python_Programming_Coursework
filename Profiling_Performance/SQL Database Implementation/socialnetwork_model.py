
# pylint: disable=W0401, W0611, W0614, C0114, E0401, C0103, E0602, R0903, C0115
import os
from peewee import *
from loguru import logger

file = 'socialnetwork.db'
#if os.path.exists(file):
#    os.remove(file)

db = SqliteDatabase(file)
#db = SqliteDatabase(':memory:')

class BaseModel(Model):

    class Meta:
        database = db

class UsersTable(BaseModel):
    """
        This class defines Users of the social network.
    """
    logger.info("creating User table in database")

    id = CharField(primary_key = True, max_length = 30, null=False)
    name = CharField(max_length = 30)
    last_name = CharField(max_length = 100)
    user_email = CharField()


class StatusTable(BaseModel):
    """
        This class defines User Status
    """

    logger.info("creating Status table in database")

    status_id = CharField(primary_key = True)
    id = ForeignKeyField(UsersTable, on_delete='CASCADE')
    status_text = CharField()
