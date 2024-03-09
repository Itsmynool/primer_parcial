from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def decrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        data = file.read()

    backend = default_backend()
    iv = data[:16]
    ciphertext = data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    decrypted_file_path = os.path.splitext(file_path)[0] + '_decrypted.txt'
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(plaintext)

    print("File decrypted successfully!")

def main():
    key = b'my_secret_key123'  # La clave debe ser la misma que la usada para encriptar
    file_path = 'mensaje_encrypted.txt'  # Nombre del archivo encriptado
    decrypt_file(file_path, key)

if __name__ == "__main__":
    main()
