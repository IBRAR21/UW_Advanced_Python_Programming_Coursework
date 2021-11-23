# pylint: disable=E0401, C0114, W0401, C0116, W0622, C0103, W0614, C0115



from unittest import TestCase
from peewee import SqliteDatabase
from socialnetwork_model import *

import users
import user_status

class TestSocialNetwork(TestCase):

    def setUp(self):
        self.database = SqliteDatabase(':memory:')
        self.database.connect()
        self.database.pragma('foreign_keys', 1, permanent=True)
        self.database.create_tables([
                UsersTable,
                StatusTable
            ])

        # Create default users
        list_of_users = [
            {'id':'abc_01', 'name':'abc', 'last_name':'xyz', 'user_email':'abc.xyz@gmail.com'},
            {'id':'mno_01', 'name':'mno', 'last_name':'qrs', 'user_email':'mno.qrs@yahoo.com'}]

        with self.database.transaction():
            UsersTable.insert_many(list_of_users).execute()

        self.user_collection = users.UserCollection(self.database)

        # Create default status

        list_of_status = [
            {'status_id':'abc_0001','id':'abc_01', 'status_text':'test message 1'},
            {'status_id':'mno_0001','id':'mno_01', 'status_text':'test message 2'},
            {'status_id':'mno_0005','id':'mno_01', 'status_text':'test message 5'}]

        with self.database.transaction():
            StatusTable.insert_many(list_of_status).execute()

        self.status_collection = user_status.UserStatusCollection(self.database)


#### user.py tests ####

    def test_add_user(self):
        test_user = self.user_collection.add_user('ijk_01', 'ijk.lmn@test.com', 'ijk', 'lmn')
        self.assertTrue(test_user)


    def test_add_duplicate_user(self):
        test_user = self.user_collection.add_user('abc_01', 'abc.xyz@test.com', 'abc', 'xyz')
        self.assertFalse(test_user)


    def test_modify_user(self):
        test_user = self.user_collection.modify_user('abc_01', 'abc.xyz@test.com', 'abc', 'xyz')
        self.assertTrue(test_user)


    def test_modify_false_user(self):
        test_user = self.user_collection.modify_user('abc_02', 'abc.xyz@test.com', 'abc', 'xyz')
        self.assertFalse(test_user)


    def test_search_user(self):
        id = 'mno_01'
        test_search = self.user_collection.search_user(id)
        self.assertTrue(test_search.id)
        self.assertTrue(test_search.name)
        self.assertTrue(test_search.last_name)
        self.assertTrue(test_search.user_email)


    def test_search_false_user(self):
        test_search = self.user_collection.search_user('abc_02')
        self.assertEqual(test_search, None)


    def test_delete_user(self):
        test_delete = self.user_collection.delete_user('abc_01')
        self.assertTrue(test_delete)


    def test_delete_false_user(self):
        test_delete = self.user_collection.delete_user('abc_04')
        self.assertFalse(test_delete)


#### user_status.py tests ####

    def test_add_status(self):
        test_status = self.status_collection.add_status('mno_0002', 'mno_01', 'test message 3')
        self.assertTrue(test_status)


    def test_add_duplicate_status(self):
        test_status = self.status_collection.add_status('mno_0001', 'mno_01', 'test message 4')
        self.assertFalse(test_status)


    def test_modify_status(self):
        test_status = self.status_collection.modify_status('mno_0001', 'mno_01', 'test message 4')
        self.assertTrue(test_status)


    def test_modify_false_status(self):
        test_status = self.status_collection.modify_status('mno_0003', 'mno_01', 'test message 4')
        self.assertFalse(test_status)


    def test_search_status(self):
        status_id = 'mno_0005'
        id = 'mno_01'
        status_text = 'test message 5'
        test_search = self.status_collection.search_status(status_id)
        self.assertTrue(test_search.status_id)
        self.assertTrue(test_search.id, id)
        self.assertTrue(test_search.status_text, status_text)


    def test_search_false_status(self):
        test_search = self.status_collection.search_status('mno_0004')
        self.assertEqual(test_search, None)


    def test_delete_status(self):
        test_delete = self.status_collection.delete_status('mno_0002')
        self.assertFalse(test_delete)


    def test_delete_false_status(self):
        test_delete = self.status_collection.delete_status('mno_0006')
        self.assertEqual(test_delete, False)


    def tearDown(self):
        self.database.drop_tables([
                UsersTable,
                StatusTable
            ])
        self.database.close()
