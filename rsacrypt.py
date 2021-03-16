from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from binascii import hexlify

"""
message = b'Hello Welcome'

enc_message = encrypt_message(message)
print(type(enc_message), '\n', enc_message)

dec_message = decrypt_message(enc_message)
print(type(dec_message), '\n', dec_message)
"""

# Encryption rsa
def encrypt_message(message):

    #Importing keys from files, converting it into the RsaKey object   
    pu_key = RSA.import_key(open('public_key.pem', 'r').read())

    #Instantiating PKCS1_OAEP object with the public key for encryption
    cipher = PKCS1_OAEP.new(key=pu_key)

    #Encrypting the message with the PKCS1_OAEP object
    cipher_text = cipher.encrypt(message)
    return cipher_text


def decrypt_message(message):
    
    #Importing keys from files, converting it into the RsaKey object 
    pr_key = RSA.import_key(open('private_key.pem', 'r').read())

    #Instantiating PKCS1_OAEP object with the private key for decryption
    decrypt = PKCS1_OAEP.new(key=pr_key)

    #Decrypting the message with the PKCS1_OAEP object
    decrypted_message = decrypt.decrypt(message)
    return decrypted_message