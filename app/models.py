from app import mongo
import bcrypt
from bson import json_util, ObjectId
import json

class User:
    @staticmethod
    def create(username, password):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        mongo.db.users.insert_one({'username': username, 'password': hashed})

    @staticmethod
    def find_by_username(username):
        return mongo.db.users.find_one({'username': username})

class Post:
    @staticmethod
    def create(title, content, author):
        result = mongo.db.posts.insert_one({'title': title, 'content': content, 'author': author})
        return result  # Return the InsertOneResult object

    @staticmethod
    def get_all():
        posts = list(mongo.db.posts.find())
        return json.loads(json_util.dumps(posts))

    @staticmethod
    def get_by_id(post_id):
        post = mongo.db.posts.find_one({'_id': ObjectId(post_id)})
        return json.loads(json_util.dumps(post)) if post else None
