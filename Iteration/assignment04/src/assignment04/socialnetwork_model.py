"""
    Database model
"""
#pylint: disable=W0614, W0401, C0103, R0903
from peewee import *

database = SqliteDatabase('socialnetwork.db')
#database = SqliteDatabase(':memory:')
database.connect()
database.pragma('foreign_keys', 1, permanent=True)

class BaseModel(Model):
    """
        BaseModel class
    """
    class Meta:
        """
            Meta class
        """
        database = database

class UsersTable(BaseModel):
    """
        Table for user accounts.
    """
    user_id = CharField(primary_key=True, max_length=30)
    user_name = CharField(max_length=30)
    user_last_name = CharField(max_length=100)
    user_email = CharField(max_length=100)

class StatusTable(BaseModel):
    """
        Table for status updates
    """
    status_id = CharField(primary_key=True, max_length=100)
    user_id = ForeignKeyField(UsersTable, on_delete='CASCADE')
    status_text = CharField(max_length=200)

# Creation of the database
database.create_tables([
        UsersTable,
        StatusTable
    ])

database.close()
