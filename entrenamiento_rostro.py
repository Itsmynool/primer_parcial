import cv2
import os
import numpy as np

def load_names():
    names = {}
    with open('names.txt', 'r') as file:
        for idx, line in enumerate(file, start=1):
            names[line.strip()] = idx
    return names

def train_face_recognizer(dataset_dir):
    # Inicializamos las listas para almacenar las imágenes y las etiquetas
    faces = []
    labels = []

    # Cargamos los nombres de las personas desde el archivo names.txt
    names = load_names()

    # Recorremos el directorio de dataset
    for root, dirs, files in os.walk(dataset_dir):
        for file in files:
            # Cargamos las imágenes en escala de grises
            img_path = os.path.join(root, file)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

            # Convertimos la imagen a un arreglo numpy
            img_np = np.array(img, 'uint8')

            # Obtenemos el nombre de la persona desde el nombre del directorio
            person_name = os.path.basename(os.path.dirname(img_path))

            # Obtenemos la etiqueta del nombre de la persona
            label = names[person_name]

            # Añadimos la imagen y la etiqueta a las listas
            faces.append(img_np)
            labels.append(label)

    # Creamos el modelo de reconocimiento facial LBPH
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Entrenamos el modelo con las imágenes y las etiquetas
    face_recognizer.train(faces, np.array(labels))

    # Guardamos el modelo entrenado en un archivo
    face_recognizer.save('trained_model.yml')

    print("Training completed successfully.")

# Directorio donde se encuentran los rostros capturados
dataset_dir = 'dataset'
train_face_recognizer(dataset_dir)
