import os
import socket
import threading
import sys
import psycopg2
from AES.aes import AES
import hash

conn = psycopg2.connect(
    dbname="chat",
    user="postgres",
    password="dimash7628",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

def login_or_register():
    nickname = input('Enter your nickname: ')
    password = input('Enter your password: ')
    

    hashed_password = hash.generate_hash(password.encode()).hex()
    # print(hashed_password)
    
  
    cursor.execute("SELECT * FROM users WHERE nickname = %s", (nickname,))
    user = cursor.fetchone()
    if user:
        if user[2] == hashed_password:
            print("Login successful!")
            return nickname
        else:
            print("Invalid password.")
            sys.exit(1)
    else:
        cursor.execute("INSERT INTO users (nickname, password) VALUES (%s, %s)", (nickname, hashed_password))
        conn.commit()
        print("User registered successfully!")
        return nickname


nickname = login_or_register()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))



secret_key = os.urandom(16)
aes = AES(b'0123456789abcdef0123456789abcdef')
iv = b'abcdefghijklmnop'

def receive(): 
    while True:
        try:
            encrypted_message = client.recv(1024)
            # Расшифровываем полученное сообщение
            decrypted_message = aes.decrypt_cbc(encrypted_message, iv)
            print(decrypted_message.decode())
        except:
            print('An error occurred!')
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {sys.stdin.readline().rstrip()}'
        # Шифруем сообщение перед отправкой
        encrypted_message = aes.encrypt_cbc(message.encode(), iv)
        client.send(encrypted_message)


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
