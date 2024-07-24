import os
import shutil
from pathlib import Path
from datetime import datetime
import time

# Configuración de nombres de carpetas
carpeta1 = "carpeta1"
carpeta2 = "carpeta2"
carpeta_duplicados = "duplicados"
carpeta_logs = "logs"

# Crear la carpeta de duplicados si no existe
if not os.path.exists(carpeta_duplicados):
    os.makedirs(carpeta_duplicados)

# Crear la carpeta de logs si no existe
if not os.path.exists(carpeta_logs):
    os.makedirs(carpeta_logs)

# Vaciar la carpeta de duplicados si contiene archivos
def vaciar_carpeta(carpeta):
    for root, dirs, files in os.walk(carpeta, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))

if os.listdir(carpeta_duplicados):
    vaciar_carpeta(carpeta_duplicados)

# Función para obtener todos los archivos en una carpeta y sus subcarpetas
def obtener_archivos(carpeta):
    archivos = []
    for root, _, files in os.walk(carpeta):
        for file in files:
            ruta_completa = os.path.join(root, file)
            archivos.append(ruta_completa)
    return archivos

# Función para calcular el tamaño de una carpeta
def calcular_tamano_carpeta(carpeta):
    tamano_total = 0
    for root, _, files in os.walk(carpeta):
        for file in files:
            ruta_completa = os.path.join(root, file)
            tamano_total += os.path.getsize(ruta_completa)
    return tamano_total

# Función para obtener la ruta relativa sin las dos primeras carpetas
def obtener_ruta_sin_dos_primeras(carpeta, archivo):
    ruta_relativa = os.path.relpath(archivo, carpeta)
    partes = ruta_relativa.split(os.sep)[1:]  # Ignorar la primera parte
    return os.sep.join(partes)

# Función para eliminar carpetas vacías
def eliminar_carpetas_vacias(carpeta):
    for root, dirs, _ in os.walk(carpeta, topdown=False):
        for dir in dirs:
            ruta_dir = os.path.join(root, dir)
            if not os.listdir(ruta_dir):  # Si la carpeta está vacía
                os.rmdir(ruta_dir)

# Obtener todos los archivos de carpeta1 y carpeta2
archivos_carpeta1 = obtener_archivos(carpeta1)
archivos_carpeta2 = obtener_archivos(carpeta2)

# Crear un diccionario para almacenar los archivos de carpeta1 con su tamaño y ruta sin las dos primeras carpetas
dic_archivos_carpeta1 = {obtener_ruta_sin_dos_primeras(carpeta1, archivo): os.path.getsize(archivo) for archivo in archivos_carpeta1}

# Obtener la fecha y hora actual para el nombre del archivo de log
fecha_hora_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(carpeta_logs, f"log_{fecha_hora_actual}.txt")

# Iniciar el contador de tiempo
start_time = time.time()

# Abrir el archivo de log para escritura
with open(log_file, 'w') as log:
    log.write(f"Log de ejecución: {fecha_hora_actual}\n\n")

    archivos_movidos = 0

    # Mover archivos duplicados de carpeta2 a la carpeta de duplicados
    for archivo2 in archivos_carpeta2:
        nombre_archivo2 = os.path.basename(archivo2)
        tamano_archivo2 = os.path.getsize(archivo2)
        ruta_relativa_sin_dos_primeras_2 = obtener_ruta_sin_dos_primeras(carpeta2, archivo2)

        # Comprobar si hay un archivo con la misma ruta relativa sin las dos primeras carpetas y tamaño en carpeta1
        if ruta_relativa_sin_dos_primeras_2 in dic_archivos_carpeta1:
            if tamano_archivo2 == dic_archivos_carpeta1[ruta_relativa_sin_dos_primeras_2]:
                # Crear la nueva ruta en la carpeta de duplicados
                nueva_ruta = os.path.join(carpeta_duplicados, ruta_relativa_sin_dos_primeras_2)
                nueva_carpeta = os.path.dirname(nueva_ruta)
                if not os.path.exists(nueva_carpeta):
                    os.makedirs(nueva_carpeta)
                # Mover el archivo
                shutil.move(archivo2, nueva_ruta)
                log_message = f"Movido: {archivo2} a {nueva_ruta}"
                print(log_message)
                log.write(log_message + "\n")
                archivos_movidos += 1

    # Eliminar carpetas vacías en carpeta2 después de mover los archivos
    eliminar_carpetas_vacias(carpeta2)

    # Calcular el tiempo transcurrido
    end_time = time.time()
    tiempo_total = end_time - start_time

    # Calcular el tamaño total de la carpeta duplicados
    tamano_total_duplicados = calcular_tamano_carpeta(carpeta_duplicados)

    # Escribir el resumen en el log
    log.write("\nResumen del proceso:\n")
    log.write(f"Total de archivos movidos: {archivos_movidos}\n")
    log.write(f"Tamaño total de la carpeta 'duplicados': {tamano_total_duplicados / (1024 * 1024):.2f} MB\n")
    log.write(f"Tiempo total del proceso: {tiempo_total:.2f} segundos\n")

print("Proceso completado.")
