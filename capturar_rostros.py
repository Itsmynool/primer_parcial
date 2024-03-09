import cv2
import os

def capture_faces():
    # Iniciamos la captura de video desde la cámara
    cap = cv2.VideoCapture(0)

    # Solicitamos al usuario que ingrese el nombre del rostro
    face_name = input('Enter the user name and press <return>: ')

    # Creamos el directorio para almacenar los rostros si no existe
    dataset_dir = os.path.join('dataset', face_name)
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)

    # Inicializamos el contador de rostros capturados
    count = 0

    while True:
        # Capturamos un frame
        ret, frame = cap.read()

        # Convertimos el frame a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Mostramos el frame
        cv2.imshow('Capture Faces', frame)

        # Detectamos caras en el frame
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # Para cada cara detectada
        for (x, y, w, h) in faces:
            # Dibujamos un rectángulo alrededor de la cara
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Incrementamos el contador de rostros capturados
            count += 1

            # Guardamos el rostro capturado en el directorio
            face_image_path = os.path.join(dataset_dir, f'{face_name}_{count}.jpg')
            cv2.imwrite(face_image_path, gray[y:y+h, x:x+w])

        # Salimos del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Salimos del bucle si se capturan 30 rostros
        if count >= 100:
            break

    # Liberamos la captura de video y cerramos todas las ventanas
    cap.release()
    cv2.destroyAllWindows()

    print(f'{count} faces captured and saved.')

    # Escribimos el nombre en el archivo names.txt
    with open('names.txt', 'a') as file:
        file.write(f'{face_name}\n')

# Capturamos y almacenamos los rostros
capture_faces()
