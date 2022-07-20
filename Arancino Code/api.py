from flask import Flask
from flask import request
from flask_cors import CORS
from Crypto.Cipher import AES
from flask import jsonify
import base64
import json
import math
import os

app = Flask(__name__)
CORS(app)


@app.route("/", methods=['POST'])
def get_current_sensor_data():
    data = request.json
    with open('sensor_data.json', 'r') as openfile:
        sensor_data = json.load(openfile)
        os.remove('sensor_data.json')
    with open('device_data.json', 'r') as openfile:
        device_data = json.load(openfile)
    final_data = jsonify({
        'sensor_data': encrypt_json_with_common_cipher(
            sensor_data, data['key'], data['byte']),
        'device_data': encrypt_json_with_common_cipher(
            device_data, data['key'], data['byte'])})
    return final_data


def encrypt_with_common_cipher(cleartext, key, byte):
    common_cipher = AES.new(key.encode(),
                            AES.MODE_CBC, byte.encode())
    cleartext_length = len(cleartext)
    nearest_multiple_of_16 = 16 * math.ceil(cleartext_length/16)
    padded_cleartext = cleartext.rjust(nearest_multiple_of_16)
    raw_ciphertext = common_cipher.encrypt(padded_cleartext)
    return base64.b64encode(raw_ciphertext).decode('utf-8')


def encrypt_json_with_common_cipher(json_obj, key, byte):
    json_string = json.dumps(json_obj)
    return encrypt_with_common_cipher(json_string.encode(), key, byte)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port='1111')
