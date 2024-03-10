import socket
import encriptado

def send_file(file_path, receiver_ip, receiver_port):
    # Crear un socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Conectar al receptor
        sock.connect((receiver_ip, receiver_port))
        
        data = encriptado.main()
        #print('DATA: ', data)

        sock.sendall(data)

    print("File sent successfully!")

if __name__ == "__main__":
    file_path = 'mensaje.txt'  # Ruta del archivo a enviar #No se usa
    receiver_ip = '192.168.1.16'  # IP del receptor
    receiver_port = 12345  # Puerto del receptor
    send_file(file_path, receiver_ip, receiver_port)
