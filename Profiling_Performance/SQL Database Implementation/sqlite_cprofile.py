# pylint: disable=C0103
import cProfile
import pstats
import main
from socialnetwork_model import *

def profile(function, *args):
    pr = cProfile.Profile()
    pr.enable()
    function(*args)
    pr.disable()

    # create stats report in metadata file format
    file = open("sqlite.txt", 'a')
    file.write(function.__name__)
    p = pstats.Stats(pr, stream=file)
    p.strip_dirs().sort_stats('cumulative').print_stats(0)
    file.close()
    return pr



if __name__ == '__main__':
    db.connect()
    db.pragma('foreign_keys', 1, permanent=True)
    db.create_tables([
        UsersTable,
        StatusTable
    ])
    user_collection = main.init_user_collection(db)
    status_collection = main.init_status_collection(db)


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

    db.close()
