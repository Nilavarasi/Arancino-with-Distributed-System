from Crypto.Cipher import AES
import base64
import json


def get_common_cipher(COMMON_ENCRYPTION_KEY, COMMON_16_BYTE_IV_FOR_AES):
    return AES.new(COMMON_ENCRYPTION_KEY,
                   AES.MODE_CBC,
                   COMMON_16_BYTE_IV_FOR_AES)


def decrypt_with_common_cipher(ciphertext, key, byte):
    common_cipher = get_common_cipher(key, byte)
    raw_ciphertext = base64.b64decode(ciphertext)
    decrypted_message_with_padding = common_cipher.decrypt(raw_ciphertext)
    return decrypted_message_with_padding.decode('utf-8').strip()


def decrypt_json_with_common_cipher(json_ciphertext, key, byte):
    json_string = decrypt_with_common_cipher(json_ciphertext, key, byte)
    return json.loads(json_string)
