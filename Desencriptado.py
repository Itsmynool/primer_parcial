from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def decrypt_file(ciphertext, key):
    data = ciphertext

    backend = default_backend()
    iv = data[:16]
    ciphertext = data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    decrypted_file_path = 'mensaje.txt'
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(plaintext)

    print("File decrypted successfully!")

def main(ciphertext):
    key = b'\x85\x19\xd7\xd5\xf4\xe4\xc7\x9f\x96\xf7\xab\x81\xfb\x8e\x0c\x84'  # La clave debe ser la misma que la usada para encriptar # Nombre del archivo encriptado
    #print('CIPHER TEXT: ', ciphertext)
    #print('CIPHER TEXT: ', ciphertext.hex())
    decrypt_file(ciphertext, key)

if __name__ == "__main__":
    main()
