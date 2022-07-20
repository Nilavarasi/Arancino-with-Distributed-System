import datetime
import pymongo
import json
import logging
from bson.json_util import dumps
from bson.objectid import ObjectId


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["DS"]


def write_data_in_db(data, tableName):
    logging.warning(myclient)
    mycol = mydb[tableName]
    data['created_at'] = datetime.datetime.now()+datetime.timedelta(2)
    return mycol.insert_one(data)


def query_data_from_db(query, tableName):
    "Find the given cipher text from given table"
    return json.loads(dumps(
        mydb[tableName].find({'cipher_text': str(query)})))


def get_user_from_db(user_id, email):
    print("user_id, email")
    print(user_id, email)
    # If the user_id is given then query using user_id
    if user_id:
        return json.loads(dumps(
            mydb['user'].find({'_id': ObjectId(user_id)})))
    # If the email is given then query using email
    elif email:
        return json.loads(dumps(
            mydb['user'].find({'email': email})))
    # If both email and user_id is not given then query all users
    else:
        return json.loads(dumps(mydb['user'].find({})))
