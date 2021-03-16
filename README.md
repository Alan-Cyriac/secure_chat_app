# secure_chat_app
A python program to interact with friends in a chatroom which have asymmetric 2 key encryption.

# how it work?
Initially, install required libraries by excuting below line:

pip install -r requirements.txt 

then, create db and table by executing pychat_db.py:

py pychat_db.py

in pychat_db.py add another user by changing the username and password in the code and execute it.

after that, create a public key and private key by executing create_pk_puk.py

lastly, run:

py server.py in a cmd

py client.py in another cmd

you can run multiple client.py in multiple cmd with several other usernames which you gave while executing pychat_db.py
