import socket

def receive_file(save_path, port):
    # Crear un socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Enlazar el socket al puerto
        sock.bind(('0.0.0.0', port))

        # Escuchar conexiones entrantes
        sock.listen()

        print("Waiting for connection...")

        # Aceptar la conexión entrante
        conn, addr = sock.accept()

        with conn:
            print('Connected by', addr)

            # Recibir el contenido del archivo
            file_data = conn.recv(1024)

            # Guardar el contenido recibido en un archivo
            with open(save_path, 'wb') as file:
                file.write(file_data)

    print("File received successfully!")

if __name__ == "__main__":
    save_path = 'ejemplo.txt'  # Ruta para guardar el archivo recibido
    port = 12345  # Puerto para escuchar conexiones
    receive_file(save_path, port)
