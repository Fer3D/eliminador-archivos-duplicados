import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
import time

# Configuración de nombres de carpetas y método de comparación
carpeta1 = "carpeta1"
carpeta2 = "carpeta2"
carpeta_duplicados = "duplicados"
carpeta_logs = "logs"

# Seleccionar el método de comparación:
# "rapido" para comparación por tamaño de archivo
# "hash" para comparación por hash SHA-256
metodo_comparacion = "hash"  # Cambia a "rapido" si prefieres la comparación por tamaño

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

# Función para calcular el hash SHA-256 de un archivo
def calcular_hash_archivo(archivo):
    hash_sha256 = hashlib.sha256()
    with open(archivo, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

# Función para obtener estadísticas de archivos
def obtener_estadisticas(carpeta):
    archivos = obtener_archivos(carpeta)
    total_archivos = len(archivos)
    tamano_total = calcular_tamano_carpeta(carpeta)
    return total_archivos, tamano_total

# Obtener todos los archivos de carpeta1 y carpeta2
archivos_carpeta1 = obtener_archivos(carpeta1)
archivos_carpeta2 = obtener_archivos(carpeta2)

if metodo_comparacion == "rapido":
    # Crear un diccionario para almacenar los archivos de carpeta1 con su tamaño y ruta sin las dos primeras carpetas
    dic_archivos_carpeta1 = {obtener_ruta_sin_dos_primeras(carpeta1, archivo): os.path.getsize(archivo) for archivo in archivos_carpeta1}
else:
    # Crear un diccionario para almacenar los archivos de carpeta1 con su hash y ruta sin las dos primeras carpetas
    dic_archivos_carpeta1 = {obtener_ruta_sin_dos_primeras(carpeta1, archivo): calcular_hash_archivo(archivo) for archivo in archivos_carpeta1}

# Obtener la fecha y hora actual para el nombre del archivo de log
fecha_hora_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(carpeta_logs, f"log_{fecha_hora_actual}.txt")

# Iniciar el contador de tiempo
start_time = time.time()

# Abrir el archivo de log para escritura
with open(log_file, 'w') as log:
    log.write(f"======== Log de Ejecución: {fecha_hora_actual} ========\n\n")

    archivos_movidos = 0

    # Mostrar estadísticas iniciales
    total_archivos1, tamano_total1 = obtener_estadisticas(carpeta1)
    total_archivos2, tamano_total2 = obtener_estadisticas(carpeta2)

    log_message = (f"Estadísticas iniciales:\n"
                   f"  - Carpeta 1: {total_archivos1} archivos, {tamano_total1 / (1024 * 1024):.2f} MB\n"
                   f"  - Carpeta 2: {total_archivos2} archivos, {tamano_total2 / (1024 * 1024):.2f} MB\n"
                   "-------------\n")
    print(log_message)
    log.write(log_message)

    # Mover archivos duplicados de carpeta2 a la carpeta de duplicados
    for archivo2 in archivos_carpeta2:
        nombre_archivo2 = os.path.basename(archivo2)
        ruta_relativa_sin_dos_primeras_2 = obtener_ruta_sin_dos_primeras(carpeta2, archivo2)
        
        if metodo_comparacion == "rapido":
            tamano_archivo2 = os.path.getsize(archivo2)
            # Comprobar si hay un archivo con la misma ruta relativa sin las dos primeras carpetas y tamaño en carpeta1
            if ruta_relativa_sin_dos_primeras_2 in dic_archivos_carpeta1:
                tamano_archivo_carpeta1 = dic_archivos_carpeta1[ruta_relativa_sin_dos_primeras_2]
                if tamano_archivo2 == tamano_archivo_carpeta1:
                    # Crear la nueva ruta en la carpeta de duplicados
                    nueva_ruta = os.path.join(carpeta_duplicados, ruta_relativa_sin_dos_primeras_2)
                    nueva_carpeta = os.path.dirname(nueva_ruta)
                    if not os.path.exists(nueva_carpeta):
                        os.makedirs(nueva_carpeta)
                    # Mover el archivo
                    shutil.move(archivo2, nueva_ruta)
                    log_message = (f"Archivo Movido:\n"
                                   f"  - Desde: {archivo2}\n"
                                   f"  - Hacia: {nueva_ruta}\n"
                                   f"Archivo duplicado encontrado en:\n"
                                   f"  - {dic_archivos_carpeta1[ruta_relativa_sin_dos_primeras_2]}\n"
                                   "-------------\n")
                    print(log_message)
                    log.write(log_message)
                    archivos_movidos += 1
        else:
            hash_archivo2 = calcular_hash_archivo(archivo2)
            # Comprobar si hay un archivo con la misma ruta relativa sin las dos primeras carpetas y hash en carpeta1
            if ruta_relativa_sin_dos_primeras_2 in dic_archivos_carpeta1:
                hash_archivo_carpeta1 = dic_archivos_carpeta1[ruta_relativa_sin_dos_primeras_2]
                if hash_archivo2 == hash_archivo_carpeta1:
                    # Crear la nueva ruta en la carpeta de duplicados
                    nueva_ruta = os.path.join(carpeta_duplicados, ruta_relativa_sin_dos_primeras_2)
                    nueva_carpeta = os.path.dirname(nueva_ruta)
                    if not os.path.exists(nueva_carpeta):
                        os.makedirs(nueva_carpeta)
                    # Mover el archivo
                    shutil.move(archivo2, nueva_ruta)
                    log_message = (f"Archivo Movido:\n"
                                   f"  - Desde: {archivo2}\n"
                                   f"  - Hacia: {nueva_ruta}\n"
                                   f"Archivo duplicado encontrado en:\n"
                                   f"  - {dic_archivos_carpeta1[ruta_relativa_sin_dos_primeras_2]}\n"
                                   "-------------\n")
                    print(log_message)
                    log.write(log_message)
                    archivos_movidos += 1

    # Eliminar carpetas vacías en carpeta2 después de mover los archivos
    eliminar_carpetas_vacias(carpeta2)

    # Calcular el tiempo transcurrido
    end_time = time.time()
    tiempo_total = end_time - start_time

    # Calcular el tamaño total de la carpeta duplicados
    tamano_total_duplicados = calcular_tamano_carpeta(carpeta_duplicados)

    # Mostrar estadísticas finales
    total_archivos_final, tamano_total_final = obtener_estadisticas(carpeta2)
    
    log_message = (f"\nEstadísticas finales:\n"
                   f"  - Carpeta 2: {total_archivos_final} archivos, {tamano_total_final / (1024 * 1024):.2f} MB\n"
                   f"  - Carpeta de duplicados: {archivos_movidos} archivos, {tamano_total_duplicados / (1024 * 1024):.2f} MB\n"
                   "-------------\n")
    print(log_message)
    log.write(log_message)

    if archivos_movidos == 0:
        no_archivos_movidos_message = "No se ha movido ningún archivo.\n"
        log.write(no_archivos_movidos_message)
        print(no_archivos_movidos_message)

    log.write("\n======== Resumen del Proceso ========\n")
    log.write(f"Total de archivos movidos: {archivos_movidos}\n")
    log.write(f"Tamaño total de la carpeta 'duplicados': {tamano_total_duplicados / (1024 * 1024):.2f} MB\n")
    log.write(f"Tiempo total del proceso: {tiempo_total:.2f} segundos\n")
    log.write("====================================\n")

print("Proceso completado.")
