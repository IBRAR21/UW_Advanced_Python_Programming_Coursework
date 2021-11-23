# pylint: disable=C0103
import cProfile
import pstats
import main
from pymongo import MongoClient

class MongoDBConnection():
    '''MongoDB Connection'''

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

def profile(function, *args):
    pr = cProfile.Profile()
    pr.enable()
    function(*args)
    pr.disable()

    # create stats report in metadata file format
    file = open("mangodb_multi_upload.txt", 'a')
    file.write(function.__name__)
    p = pstats.Stats(pr, stream=file)
    p.strip_dirs().sort_stats('cumulative').print_stats(0)
    file.close()
    return pr



if __name__ == '__main__':

    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.SocialNetwork
        UserAccounts = database['UserAccounts']
        StatusUpdates = database['StatusUpdates']
        user_collection = main.init_user_collection(database)
        status_collection = main.init_status_collection(database)


        profile(main.load_users, "accounts.csv", user_collection)
        profile(main.load_status_updates, "status_updates.csv", status_collection)
        profile(main.add_user, "userid", "email", "name", "last_name", user_collection)
        profile(main.add_status, "userid", "statusid", "text", status_collection)
        profile(main.update_user, "userid", "email", "name", "last_name", user_collection)
        profile(main.update_status, "statusid", "userid", "text", status_collection)
        profile(main.search_user, "userid", user_collection)
        profile(main.search_status, "statusid", status_collection)
        profile(main.delete_status, "statusid", status_collection)
        profile(main.delete_user, "userid", user_collection)

        UserAccounts.drop()
        StatusUpdates.drop()
