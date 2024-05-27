import cv2
import os

# Directorio donde se guardarán las imágenes
directorio_guardado = "C:\\Imagenes"

# Inicializar el clasificador de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Inicializar la ventana de visualización
cv2.namedWindow("Captura de Rostros")

# Capturar video desde la cámara
cap = cv2.VideoCapture(0)

# Contador para el nombre de los archivos
contador = 0

# Cantidad mínima de fotos a capturar
min_fotos = 100

# Etiqueta única para todas las imágenes
etiqueta = None

while True:
    # Leer un frame de video
    ret, frame = cap.read()

    # Convertir el frame a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar rostros en el frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Para cada rostro detectado
    for (x, y, w, h) in faces:
        # Dibujar un rectángulo alrededor del rostro detectado
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Guardar el rostro en una imagen
        rostro = frame[y:y+h, x:x+w]

        # Guardar el rostro como una imagen en el directorio de guardado
        nombre_archivo = os.path.join(directorio_guardado, f"rostro_{contador}.jpg")
        cv2.imwrite(nombre_archivo, rostro)

        # Incrementar el contador para el siguiente archivo
        contador += 1

        # Verificar si se han capturado suficientes fotos
        if contador >= min_fotos:
            break

    # Muestra el frame
    cv2.imshow("Captura de Rostros", frame)

    # Sale del bucle si se han capturado suficientes fotos
    if contador >= min_fotos:
        break

    # Sale del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la captura de video y cierra la ventana
cap.release()
cv2.destroyAllWindows()

# ingrese una etiqueta única para todas las imágenes
etiqueta = input("Ingrese una etiqueta para todas las imágenes capturadas: ")

# Renombrar todas las imágenes con la etiqueta ingresada
for i in range(contador):
    nombre_original = os.path.join(directorio_guardado, f"rostro_{i}.jpg")
    nombre_nuevo = os.path.join(directorio_guardado, f"{etiqueta}_{i}.jpg")
    os.rename(nombre_original, nombre_nuevo)

print(f"Todas las imágenes se han etiquetado como '{etiqueta}' y se han guardado en {directorio_guardado}.")
