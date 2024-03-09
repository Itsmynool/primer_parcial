from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        plaintext = file.read()

    backend = default_backend()
    iv = os.urandom(16)  # Initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    encrypted_file_path = os.path.splitext(file_path)[0] + '_encrypted.txt'
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(iv + ciphertext)

    print("File encrypted successfully!")

def main():
    key = b'my_secret_key123'  # La clave debe tener 16, 24, o 32 bytes
    file_path = 'mensaje.txt'  # Asegúrate de tener este archivo en la misma ruta
    encrypt_file(file_path, key)

if __name__ == "__main__":
    main()
