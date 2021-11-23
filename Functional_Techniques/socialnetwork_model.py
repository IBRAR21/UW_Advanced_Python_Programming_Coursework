
# pylint: disable=W0401, W0611, W0614, C0114, E0401, C0103, E0602, R0903, C0115
import os
from peewee import *
from playhouse.dataset import DataSet
from loguru import logger

file = 'socialnetwork.db'
# if os.path.exists(file):
#    os.remove(file)

ds = DataSet('sqlite:///' + file)

#create table for users
User_table = ds["UsersTable"]
User_table.insert(user_id='test',
             user_name='test_1',
             user_last_name='test_2',
             email='test_3')
User_table.create_index(['user_id'], unique=True)
User_table.delete(user_id='test',
             user_name='test_1',
             user_last_name='test_2',
             email='test_3')
logger.debug("User Table created in dataset")

#create table for user status
Status_table = ds["StatusTable"]
Status_table.insert(status_id='test01',
             user_id='test',
             status_text='test message')
Status_table.create_index(['status_id'], unique=True)
Status_table.delete(status_id='test01',
             user_id='test',
             status_text='test message')
logger.debug("Status Table created in dataset")
