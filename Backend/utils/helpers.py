from flask import jsonify
import random


def getUserFromDB(user_in_db, db):
    if len(user_in_db) > 0:
        user_in_db = user_in_db[0]
        user_in_db['user_id'] = user_in_db['_id']['$oid']
        # Delete password, _id, private key, so that
        # it will not be sent to frontend
        user_in_db.pop('_id')
        user_in_db.pop('password')
        return jsonify({'data': user_in_db})
    else:
        return jsonify({'data': 'error'})


def createSecret():
    return(
        str(random.randint(1000, 9999)) +
        str(random.randint(1000, 9999)) +
        str(random.randint(1000, 9999)) +
        str(random.randint(1000, 9999))
    )
