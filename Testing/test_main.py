import main
import users
import user_status
from unittest import TestCase

class Test_Main(TestCase):
    def setUp(self):
        self.user_collection = main.init_user_collection()
        self.status_collection = main.init_status_collection()

    def test_init_user_collection(self):
        test_collection = main.init_user_collection()
        self.assertEqual(test_collection.database, {})

    def test_init_status_collection(self):
        test_collection = main.init_status_collection()
        self.assertEqual(test_collection.database, {})

    def test_load_status_updates(self):
        self.assertEqual(main.load_status_updates("status_updates.csv", self.status_collection), True)

    def test_save_status_updates(self):
        main.load_status_updates("status_updates.csv", self.status_collection)
        self.assertEqual(main.save_status_updates("new_status_updates.csv", self.status_collection), True)

    def test_load_users(self):
        self.assertEqual(main.load_users("accounts.csv", self.user_collection), True)

    def test_save_users(self):
        main.load_users("accounts.csv", self.user_collection)
        self.assertEqual(main.save_users("new_accounts.csv", self.user_collection), True)

    def test_add_user(self):
        self.assertEqual(main.add_user("MJames", "mjames12@gmail.com", "Mary", "James", self.user_collection), True)

    def test_update_user(self):
        main.add_user("MJames", "mjames12@gmail.com", "Mary", "James", self.user_collection)
        self.assertEqual(main.update_user("MJames", "mjames12@yahoo.com", "Mary", "James", self.user_collection), True)

    def test_delete_user(self):
        main.add_user("MJames", "mjames12@gmail.com", "Mary", "James", self.user_collection)
        self.assertEqual(main.delete_user("MJames", self.user_collection), True)

    def test_search_user(self):
        test_user = users.Users("MJames", "mjames12@gmail.com", "Mary", "James")
        main.add_user("MJames", "mjames12@gmail.com", "Mary", "James", self.user_collection)
        search_result = main.search_user("MJames", self.user_collection)
        self.assertEqual(search_result.user_id, test_user.user_id)
        self.assertEqual(search_result.email, test_user.email)
        self.assertEqual(search_result.user_name, test_user.user_name)
        self.assertEqual(search_result.user_last_name, test_user.user_last_name)

    def test_add_status(self):
        self.assertEqual(main.add_status("MJames_00001", "MJames", "Hope this works", self.status_collection), True)

    def test_update_status(self):
        main.add_status("MJames_00001", "MJames", "Looks like this works!", self.status_collection)
        self.assertEqual(main.update_status("MJames_00001", "MJames", "Looks like this works!", self.status_collection), True)

    def test_delete_status(self):
        main.add_status("MJames_00001", "MJames", "Hope this works", self.status_collection)
        self.assertEqual(main.delete_status("MJames_00001", self.status_collection), True)

    def test_search_status(self):
        test_status = user_status.UserStatus("MJames_00001", "MJames", "Hope this works")
        main.add_status("MJames_00001", "MJames", "Hope this works", self.status_collection)
        search_result = main.search_status("MJames_00001", self.status_collection)
        self.assertEqual(search_result.status_id, test_status.status_id)