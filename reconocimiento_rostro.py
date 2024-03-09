import cv2

def load_names():
    names = {}
    with open('names.txt', 'r') as file:
        for idx, line in enumerate(file, start=1):
            names[idx] = line.strip()
    return names

def recognize_faces():
    # Cargamos el clasificador de reconocimiento facial de OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read('trained_model.yml')

    # Cargamos el mapeo de nombres
    names = load_names()

    # Definimos un umbral de confianza
    confidence_threshold = 60

    # Iniciamos la captura de video desde la cámara
    cap = cv2.VideoCapture(0)

    while True:
        # Capturamos un frame
        ret, frame = cap.read()

        # Volteamos horizontalmente el frame para aplicar el efecto espejo
        frame = cv2.flip(frame, 1)

        # Convertimos el frame a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectamos caras en el frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # Para cada cara detectada
        for (x, y, w, h) in faces:
            # Realizamos el reconocimiento facial
            label, confidence = face_recognizer.predict(gray[y:y+h, x:x+w])

            # Si la confianza es alta y la etiqueta está en el diccionario de nombres
            if label in names and confidence < confidence_threshold:
                name = names[label]
            else:
                name = 'Desconocido'
            
            # Mostramos el nombre de la persona
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            
            # Dibujamos un rectángulo alrededor de la cara
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Mostramos el frame
        cv2.imshow('Face Recognition', frame)

        # Salimos del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberamos la captura de video y cerramos todas las ventanas
    cap.release()
    cv2.destroyAllWindows()

# Realizamos el reconocimiento facial
recognize_faces()
