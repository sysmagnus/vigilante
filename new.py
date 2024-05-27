# -*- coding: utf-8 -*-
"""
Created on Sun May 19 18:53:32 2024

@author: usuario
"""
  #C:\Users\kaito\.spyder-py3
import face_recognition
import cv2
import os
import sqlite3
from datetime import datetime

# Función para crear la tabla si no existe
def crear_tabla():
    # Conexión a la base de datos (si no existe, se crea automáticamente)
    conn = sqlite3.connect('registros_identificacion.db')
    cursor = conn.cursor()

    # Crear tabla si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS registros (
                        id INTEGER PRIMARY KEY,
                        nombre TEXT,
                        fecha TEXT,
                        hora TEXT,
                        minuto TEXT
                    )''')

    # Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()

#  insertar un nuevo registro
def insertar_registro(nombre, fecha, hora, minuto):
    # Conexión a la base de datos
    conn = sqlite3.connect('registros_identificacion.db')
    cursor = conn.cursor()

    # Insertar registro en la tabla
    cursor.execute('''INSERT INTO registros (nombre, fecha, hora, minuto)
                      VALUES (?, ?, ?, ?)''', (nombre, fecha, hora, minuto))

    # Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()

# verificar si una persona ya ha sido registrada hoy
def esta_registrado_hoy(nombre, fecha):
    # Conexión a la base de datos
    conn = sqlite3.connect('registros_identificacion.db')
    cursor = conn.cursor()

    # Verificar si la persona ya ha sido registrada hoy
    cursor.execute('''SELECT * FROM registros WHERE nombre = ? AND fecha = ?''', (nombre, fecha))
    registro = cursor.fetchone()

    # Cerrar conexión
    conn.close()

    return registro is not None

# Crear tabla si no existe
crear_tabla()

# Directorio donde se encuentran las imágenes
directorio = "C:\\Imagenes"

# Cargar imágenes y sus nombres
imagenes = []
nombres = []
for filename in os.listdir(directorio):
    if filename.endswith(".jpg") or filename.endswith(".png"):  
        img = face_recognition.load_image_file(os.path.join(directorio, filename))
        imagenes.append(img)
        nombres.append(os.path.splitext(filename)[0])

# Encuentra codificaciones faciales para todas las caras en la lista de imágenes
codificaciones_conocidas = []
for img in imagenes:
    face_encodings = face_recognition.face_encodings(img)
    if len(face_encodings) > 0:
        codificaciones_conocidas.append(face_encodings[0])
    else:
        print("No se pudo encontrar ninguna cara en la imagen:", img)

# Inicializar el clasificador de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Inicializar la ventana de visualización
cv2.namedWindow("Ventana de reconocimiento")

# Capturar video desde la cámara
cap = cv2.VideoCapture(0)

# Bucle principal
while True:
    # Leer un frame de video
    ret, frame = cap.read()

    # Convertir el frame a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar rostros en el frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Para cada rostro detectado, intentar reconocerlo
    for (x, y, w, h) in faces:
        # Codificar el rostro detectado
        face_encodings = face_recognition.face_encodings(frame, [(y, x+w, y+h, x)])

        # Inicializar el flag de reconocimiento de rostro
        reconocido = False

        # Comparar el rostro codificado con los rostros conocidos
        for face_encoding in face_encodings:
            # Compara el rostro codificado con todos los rostros conocidos
            matches = face_recognition.compare_faces(codificaciones_conocidas, face_encoding)

            # Si encuentra un rostro conocido
            if True in matches:
                nombre = nombres[matches.index(True)]
                cv2.putText(frame, nombre, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                reconocido = True

                # Obtener la fecha y hora actuales
                fecha_actual = datetime.now().strftime('%Y-%m-%d')
                hora_actual = datetime.now().strftime('%H:%M:%S')
                minuto_actual = datetime.now().strftime('%M')

                # Verificar si la persona ya ha sido registrada hoy
                if not esta_registrado_hoy(nombre, fecha_actual):
                    # Insertar registro en la base de datos
                    insertar_registro(nombre, fecha_actual, hora_actual, minuto_actual)

        # Si no se reconoció ningún rostro
        if not reconocido:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(frame, "Desconocido", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 2)

    # Muestra el frame
    cv2.imshow("Ventana de reconocimiento", frame)

    # Sale del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la captura de video y cierra la ventana
cap.release()
cv2.destroyAllWindows()
