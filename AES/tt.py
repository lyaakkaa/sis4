import os
from aes import AES


aes = AES(b'0123456789abcdef0123456789abcdef')

# secret_key = os.urandom(16)
# aes = AES(secret_key)
# aes = AES(b'0123456789abcdef0123456789abcdef')
# iv = bytes(16)

message = b'Hello, world!'

iv = b'abcdefghijklmnop'

encrypted_message = aes.encrypt_cbc(message, iv)
decrypted_message = aes.decrypt_cbc(encrypted_message, iv)

print("Зашифрованное сообщение:", encrypted_message)
print("Расшифрованное сообщение: ", decrypted_message)
