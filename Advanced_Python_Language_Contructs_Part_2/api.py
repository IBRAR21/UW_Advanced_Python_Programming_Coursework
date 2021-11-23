from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask import jsonify
from menu import dataset_connection
import socialnetwork_model as snm
from list_user_images import reconcile_images

connection_type = "sqlite:///socialnetwork.db"
db_connect = create_engine(connection_type)

class Users(Resource):
    def get(self):
        conn = db_connect.connect()
        result = {}
        query = conn.execute("select * from UsersTable")
        for i in query.cursor:
            user = dict(zip(tuple(query.keys()), i))
            user_id = user.pop('user_id')
            statuses = conn.execute(f'SELECT status_text FROM StatusTable WHERE user_id = "{user_id}"')
            user['status_updates'] = [status[0] for status in statuses.cursor]
            result[user_id] = user
        conn.close()
        return jsonify(result)

class Images(Resource):
    def get(self):
        conn = db_connect.connect()
        result = {}
        query = conn.execute("select user_id from UsersTable")
        for user in query.cursor:
            user_id = user[0]
            images = conn.execute(f'SELECT tags, id FROM PictureTable WHERE user_id = "{user_id}"')
            result = {
            user_id : [dict(zip(tuple(images.keys()), i)) for i in images.cursor]}
        conn.close()
        return jsonify(result)

class Differences(Resource):
    def get(self):
        conn = db_connect.connect()
        result = {}
        query = conn.execute("select user_id from UsersTable")
        for user in query.cursor:
            user_id = user [0]
            difference = reconcile_images(user_id, user_collection, image_collection)
            if difference:
                result[user_id] = difference
        conn.close()
        return jsonify(result)

def setup(name=__name__):

    app = Flask(name)
    api = Api(app)
    api.add_resource(Users, "/users")
    api.add_resource(Images, "/images")
    api.add_resource(Differences, "/differences")
    return app

if __name__ == "__main__":
    with dataset_connection(connection_type) as db:
        user_collection, status_collection, image_collection = snm.create_tables(db)
        app = setup()
        app.run(port="5002")
        db_connect.dispose()