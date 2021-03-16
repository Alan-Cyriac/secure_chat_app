"""
To create public and private key
"""

# Alan Cyriac

from Cryptodome.PublicKey import RSA
import os

def create_cred_keys():
    
    """
    To create public and private key
    """
    
    key = RSA.generate(2048)

    # Write private key
    private_key = key.export_key("PEM")
    with open('private_key.pem', "wb") as fd:
        fd.write(private_key)
    os.chmod('private_key.pem', 0o600)

    # Write public key
    public_key = key.publickey().export_key("OpenSSH")
    with open('public_key.pem', "wb") as fd:
        fd.write(public_key)
    os.chmod('public_key.pem', 0o600)

    
create_cred_keys()
