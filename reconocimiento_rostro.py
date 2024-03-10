import cv2
import time
import Desencriptado

def load_names():
    names = {}
    with open('names.txt', 'r') as file:
        for idx, line in enumerate(file, start=1):
            names[idx] = line.strip()
    return names

def load_face_recognition_model():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read('trained_model.yml')

    return face_cascade, face_recognizer

def recognize_faces():
    # Cargamos el clasificador de reconocimiento facial de OpenCV
    face_cascade, face_recognizer = load_face_recognition_model()
    # Cargamos el mapeo de nombres
    names = load_names()
    # Definimos un umbral de confianza
    confidence_threshold = 60
    # Iniciamos la captura de video desde la cámara
    cap = cv2.VideoCapture(0)

    recognized_time = None
    unrecognized_time = None
    recognized_person = None
    undetected_face = None

    access = False

    while True:
        # Capturamos un frame
        ret, frame = cap.read()
        # Volteamos horizontalmente el frame para aplicar el efecto espejo
        frame = cv2.flip(frame, 1)
        # Convertimos el frame a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detectamos caras en el frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        #print('FACES: ', faces)
        #print('Names: ', names)
        # Si hay al menos una cara detectada
        if len(faces) > 0:
            # Para cada cara detectada
            for (x, y, w, h) in faces:
                # Realizamos el reconocimiento facial
                label, confidence = face_recognizer.predict(gray[y:y+h, x:x+w])
                # Si la confianza es alta y la etiqueta está en el diccionario de nombres
                if label in names and confidence < confidence_threshold:
                    recognized_person = names[label]
                    if recognized_time is None:
                        if unrecognized_time is not None:
                            unrecognized_time = None
                        if undetected_face is not None:
                            undetected_face = None
                        recognized_time = time.time()  # Iniciar el contador si no ha comenzado

                else:
                    recognized_person = "Desconocido"
                    if unrecognized_time is None:
                        if recognized_time is not None:
                            recognized_time = None
                        if undetected_face is not None:
                            undetected_face = None
                        unrecognized_time = time.time()

                # Dibujar un rectángulo alrededor de la cara
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                # Mostrar el nombre o "Desconocido" en el cuadro de la persona detectada
                cv2.putText(frame, recognized_person, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

        # Mostrar el frame
        cv2.imshow('Face Recognition', frame)

        #print('TIEMPO RECONOCIDO: ', recognized_time)
        #print('TIEMPO NO RECONOCIDO: ', unrecognized_time)

        #print('RECOGNIZED TIME: ', recognized_time)
        #print('UNRECOGNIZED TIME: ', unrecognized_time)
        #and ((recognized_time is not None) or (unrecognized_time is not None))
        if recognized_time is None and unrecognized_time is None and undetected_face is None:
            undetected_face = time.time()

        if recognized_time is not None:
            recognized_time_mapping = time.time() - recognized_time
            #print('RECOGNIZED: ', recognized_time_mapping)
            if recognized_time_mapping >= 3:
                print('Access grantied')
                access = True
                break
        elif unrecognized_time is not None:
            unrecognized_time_mapping = time.time() - unrecognized_time
            #print('UNRECOGNIZED: ', unrecognized_time_mapping)
            if unrecognized_time_mapping >= 3:
                print('Access denied')
                break
        elif undetected_face is not None:
            undetected_face_mapping = time.time() - undetected_face
            #print('TIME OUT: ', undetected_face_mapping)
            if undetected_face_mapping >= 5:
                print('Timeout')
                break

        # Si no se detecta ningún rostro, reiniciar el contador
        if len(faces) == 0:
            recognized_time = None
            unrecognized_time = None

        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar la captura de video y cerrar todas las ventanas
    cap.release()
    cv2.destroyAllWindows()

    if access:
        Desencriptado.main()

# Realizar el reconocimiento facial
recognize_faces()
