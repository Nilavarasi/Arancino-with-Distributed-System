from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from utils import db
from utils import helpers
from utils import decyrpt
import json
import requests
import os
from web3 import Web3, HTTPProvider
from interface import ContractInterface
from utils import excel


w3 = Web3(HTTPProvider('http://127.0.0.1:8545'))
# with open("deployment_variables.json", 'r') as f:
#     datastore = json.load(f)
#     abi = datastore["contract_abi"]
#     contract_address = datastore["contract_address"]


contract_dir = os.path.abspath('./contracts/')
greeter_interface = ContractInterface(w3, 'StoreSensorData', contract_dir)
greeter_interface.compile_source_files()
greeter_interface.deploy_contract()
instance = greeter_interface.get_instance()


# instance = w3.eth.contract(address=contract_address, abi=abi)


app = Flask(__name__)
CORS(app)


@app.route("/register", methods=['POST'])
def register():
    data = request.json
    api_key = data['api_key']
    user_name = data['user_name']
    password = data['password']
    email = data['email']
    is_admin = True
    db_data = {
        "user_name": user_name,
        "password": password,
        "email": email,
        "is_admin": is_admin
    }
    db.write_data_in_db(db_data, "user")
    return jsonify({"data": "success", "status": 200})


@app.route("/login", methods=['POST'])
def login():
    print("data")
    print(request.data)
    data = request.json
    user_in_db = db.get_user_from_db(
        user_id=None, email=data['email'])
    print("user_in_db", user_in_db)
    if user_in_db and (data['password'] != user_in_db[0]['password']):
        return jsonify({'data': 'incorrect password'})
    return helpers.getUserFromDB(user_in_db=user_in_db, db=db)


@app.route("/register_board_details", methods=['POST'])
def register_board():
    data = request.json
    user = db.get_user_from_db(user_id=None, email=data['email'])
    if len(user) > 0 and user[0]['is_admin']:
        instance.functions.putBoardDetails(
            data['board_id'], data['board_name']).transact()
        instance.functions.putPluginDetails(
            data['plugin_id'], data['plugin_name']).transact()
        return jsonify({"data": "success", "status": 200})
    else:
        jsonify({"data": "UnAuthorized", "status": 400})


@app.route("/register_sensor_data", methods=['GET'])
def register_sensor_data():

    secret_key = helpers.createSecret()
    byte = helpers.createSecret()
    url = "http://18.234.188.99:1111/"
    payload = json.dumps({
        "key": str(secret_key),
        "byte": str(byte)
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    result = response.json()
    secret_key = secret_key.encode()
    byte = byte.encode()
    decrypted_device_json = decyrpt.decrypt_json_with_common_cipher(
        result['device_data'].encode(), secret_key, byte)
    decrypted_sensor_json = decyrpt.decrypt_json_with_common_cipher(
        result['sensor_data'].encode(), secret_key, byte)
    date = list(decrypted_sensor_json.keys())
    sensor_data = list(decrypted_sensor_json.values())
    # Store the decrypted data in blockchain
    for i in range(1, len(date)):
        print(str(date[i]), str(sensor_data[i]))
        instance.functions.putSensorData(
            str(date[i]), str(sensor_data[i])).transact()
    excel_data = []
    # Store the data in excel
    # [[d1, v1], [d2, v2], [d3, v3]]
    for i in range(1, len(date)):
        excel_data.append([date[i], sensor_data[i]])
    excel.write_data_in_excel(excel_data)
    return decrypted_device_json


@app.route("/get_sensor_data", methods=["GET"])
def getData():
    data = instance.functions.getData().call()
    print("data")
    print(data)
    return jsonify({"data": data, "status": 200})


@app.route("/get_recent_data", methods=["GET"])
def getRecentData():
    recent_data = []
    length = instance.functions.getTotaLength().call()
    for i in range(length-8, length):
        data = instance.functions.getIndexData(i).call()
        recent_data.append({'date': data[0], 'sensor_data': data[1]})
    return jsonify({"recent_data": recent_data})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port='2221')
