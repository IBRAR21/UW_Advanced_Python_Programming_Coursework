# pylint: disable=E0401, C0114, W0401, C0116, W0622, C0103, W0614, C0115
# pylint: disable=C0301, E0602, W1309, R0904, R0801

from unittest import TestCase
import peewee
from playhouse.dataset import DataSet
import users
import user_status
import list_user_images

class TestSocialNetwork(TestCase):

    def setUp(self):
        self.database = DataSet('sqlite:///:memory:')

        #create table for users
        User_table = self.database["UsersTable"]
        User_table.insert(user_id='test',
                          user_name='test_1',
                          user_last_name='test_2',
                          email='test_3')
        User_table.create_index(['user_id'], unique=True)
        User_table.delete(user_id='test',
                          user_name='test_1',
                          user_last_name='test_2',
                          email='test_3')

        #create table for user status
        Status_table = self.database["StatusTable"]
        Status_table.insert(status_id='test01',
                            user_id='test',
                            status_text='test message')
        Status_table.create_index(['status_id'], unique=True)
        Status_table.delete(status_id='test01',
                            user_id='test',
                            status_text='test message')

        # create table for user status
        Picture_table = self.database["PictureTable"]
        Picture_id = Picture_table.insert(user_id='test',
                            tags='#test')
        Picture_table.delete(id = Picture_id,
                            user_id='test',
                            tags='#test')

        # Create default users
        list_of_users = [
            {'USER_ID':'abc_01', 'NAME':'abc', 'LASTNAME':'xyz', 'EMAIL':'abc.xyz@gmail.com'},
            {'USER_ID':'mno_01', 'NAME':'mno', 'LASTNAME':'qrs', 'EMAIL':'mno.qrs@yahoo.com'}]

        for user in list_of_users:
            try:
                User_table.insert(user_id = user['USER_ID'],
                                  user_name = user['NAME'],
                                  user_last_name = user['LASTNAME'],
                                  email = user['EMAIL'])
            except peewee.IntegrityError:
                logger.warning(f"user_id:{user_id} already existed. Duplicate entry cannot be made.")

        self.user_collection = User_table

        # Create default status

        list_of_status = [
            {'STATUS_ID':'abc_0001','USER_ID':'abc_01', 'STATUS_TEXT':'test message 1'},
            {'STATUS_ID':'mno_0001','USER_ID':'mno_01', 'STATUS_TEXT':'test message 2'},
            {'STATUS_ID':'mno_0005','USER_ID':'mno_01', 'STATUS_TEXT':'test message 5'}]

        for status in list_of_status:
            try:
                Status_table.insert(status_id = status['STATUS_ID'],
                                    user_id = status['USER_ID'],
                                    status_text = status['STATUS_TEXT'])
            except peewee.IntegrityError:
                logger.warning(f"status_id:{row['STATUS_ID']} already existed. Duplicate entry cannot be made.")

        self.status_collection = Status_table

        # create default pictures

        list_of_images = [
            {'USER_ID': 'abc_01', 'Tag': '#car #sport'},
            {'USER_ID': 'mno_01', 'Tag': '#car #luxury'}]

        for image in list_of_images:
            try:
                image_id = Picture_table.insert(user_id=image['USER_ID'],
                                    tags = image['Tag'])
                list_user_images.create_picture_file(image['USER_ID'], image_id, image['Tag'])
            except peewee.IntegrityError:
                logger.warning(f"Error occured while creating image.")

        # create unique image on database
        Picture_table.insert(user_id='mno_01',
                                        tags='#travel')

        self.image_collection = Picture_table


#### user.py tests ####

    def test_add_user(self):
        test_user = users.add_user('ijk_01', 'ijk.lmn@test.com', 'ijk', 'lmn', self.user_collection)
        self.assertTrue(test_user)


    def test_add_duplicate_user(self):
        test_user = users.add_user('abc_01', 'abc.xyz@test.com', 'abc', 'xyz', self.user_collection)
        self.assertFalse(test_user)


    def test_modify_user(self):
        test_user = users.modify_user('abc_01', 'abc.xyz@test.com', 'abc', 'xyz', self.user_collection)
        self.assertTrue(test_user)


    def test_modify_false_user(self):
        test_user = users.modify_user('abc_02', 'abc.xyz@test.com', 'abc', 'xyz', self.user_collection)
        self.assertFalse(test_user)


    def test_search_user(self):
        id = 'mno_01'
        test_search = users.search_user(id, self.user_collection)
        self.assertTrue(test_search['user_id'])
        self.assertTrue(test_search['user_name'])


    def test_search_false_user(self):
        test_search = users.search_user('abc_02', self.user_collection)
        self.assertEqual(test_search, None)


    def test_delete_user(self):
        test_delete = users.delete_user('abc_01', self.user_collection, self.status_collection)
        self.assertTrue(test_delete)


    def test_delete_false_user(self):
        test_delete = users.delete_user('abc_04', self.user_collection, self.status_collection)
        self.assertFalse(test_delete)


#### user_status.py tests ####

    def test_add_status(self):
        test_status = user_status.add_status('mno_0002', 'mno_01', 'test message 3', self.user_collection, self.status_collection)
        self.assertTrue(test_status)


    def test_add_duplicate_status(self):
        test_status = user_status.add_status('mno_0001', 'mno_01', 'test message 4', self.user_collection, self.status_collection)
        self.assertFalse(test_status)


    def test_modify_status(self):
        test_status = user_status.modify_status('mno_0001', 'mno_01', 'test message 4', self.user_collection, self.status_collection)
        self.assertTrue(test_status)


    def test_modify_false_status(self):
        test_status = user_status.modify_status('mno_0003', 'mno_01', 'test message 4', self.user_collection, self.status_collection)
        self.assertFalse(test_status)


    def test_search_status(self):
        status_id = 'mno_0005'
        user_id = 'mno_01'
        status_text = 'test message 5'
        test_search = user_status.search_status(status_id, self.status_collection)
        self.assertTrue(test_search['status_id'])
        self.assertTrue(test_search['user_id'], user_id)
        self.assertTrue(test_search['status_text'], status_text)


    def test_search_false_status(self):
        test_search = user_status.search_status('mno_0004', self.status_collection)
        self.assertEqual(test_search, None)


    def test_delete_status(self):
        test_delete = user_status.delete_status('mno_0002', self.status_collection)
        self.assertFalse(test_delete)


    def test_delete_false_status(self):
        test_delete = user_status.delete_status('mno_0006', self.status_collection)
        self.assertEqual(test_delete, False)

#### list_user_images.py tests ####
    def test_add_image(self):
        test_image = list_user_images.add_image('mno_01', '#car #luxury', self.user_collection, self.image_collection)
        self.assertTrue(test_image)

    def test_add_image_incorrect_tag(self):
        test_image = list_user_images.add_image('mno_01', '#car #1234', self.user_collection, self.image_collection)
        self.assertFalse(test_image)

    def test_list_of_user_images(self):
        user_id = 'abc_01'
        result = list_user_images.list_of_user_images(user_id)
        self.assertEqual(len(result), 1)

    def test_reconcile_images_no_difference(self):
        user_id = 'mno_01'
        result = list_user_images.reconcile_images(user_id, self.user_collection, self.image_collection)
        self.assertEqual(result[0], [])

    def test_reconcile_images_difference(self):
        user_id = 'mno_01'
        result = list_user_images.reconcile_images(user_id, self.user_collection, self.image_collection)
        self.assertTrue(result[1])

    def test_reconcile_images_false(self):
        user_id = 'mno01'
        result = list_user_images.reconcile_images(user_id, self.user_collection, self.image_collection)
        self.assertFalse(result)

    def tearDown(self):
        self.database.close()
