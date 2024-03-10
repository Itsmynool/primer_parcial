from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import time

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        plaintext = file.read()

    backend = default_backend()
    iv = os.urandom(16)  # Initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    encrypted_content = iv + ciphertext
    #print("Encrypted content:")
    #print(encrypted_content.decode('latin1'))  # Decode as latin1 to handle binary data
    return encrypted_content

def main():
    key = b'\x85\x19\xd7\xd5\xf4\xe4\xc7\x9f\x96\xf7\xab\x81\xfb\x8e\x0c\x84'
    file_path = 'mensaje.txt' 
    encrypted_content = None

    while encrypted_content is None:
        try:
            encrypted_content = encrypt_file(file_path, key)
        except Exception as e:
            print("Error:", e)
            print("Retrying in 1 second...")
            time.sleep(1)

    print("Encryption completed!")

    return encrypted_content.decode('latin1')

if __name__ == "__main__":
    main()
