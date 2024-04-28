from aes import AES
import os
import pathlib

def read_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def write_file(file_path, data):
    with open(file_path, 'wb') as file:
        file.write(data)

def main():
    input_file_name = input("Enter the name of the file to encrypt: ")

    input_file_path = input_file_name
    file_extension = pathlib.Path(input_file_path).suffix  # Extracting file extension

    encrypted_file_path = f"{input_file_name}_encrypted.aes"
    decrypted_file_path = f"{input_file_name}_decrypted_file{file_extension}"  # Append file extension

    secret_key = os.urandom(16)
    aes = AES(secret_key)

    plaintext = read_file(input_file_path)

    ciphertext = aes.encrypt_cbc(plaintext, iv=bytes(16))  # You can choose a different IV

    # Save the encrypted content to a new file
    write_file(encrypted_file_path, ciphertext)
    print(f"Encrypted file saved at: {encrypted_file_path}")

    # Read the encrypted file
    encrypted_content = read_file(encrypted_file_path)

    # Decrypt the content
    decrypted_content = aes.decrypt_cbc(encrypted_content, iv=bytes(16))

    # Save the decrypted content to a new file with the original file extension
    write_file(decrypted_file_path, decrypted_content)
    print(f"Decrypted file saved at: {decrypted_file_path}")

if __name__ == "__main__":
    main()