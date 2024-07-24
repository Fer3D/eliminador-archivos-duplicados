# Script de Mantenimiento de Archivos Duplicados

## Descripción

Este script en Python está diseñado para gestionar archivos duplicados entre dos carpetas (`carpeta1` y `carpeta2`). Su función principal es identificar archivos en `carpeta2` que ya existen en `carpeta1` (considerando el nombre del archivo y el tamaño o hash) y mover estos archivos duplicados a una carpeta específica llamada `duplicados`. Además, elimina carpetas vacías en `carpeta2` después de mover los archivos. Los eventos y resultados del proceso se registran en un archivo de log, que se guarda en una carpeta `logs`.

## Funcionalidades

1. **Creación de Carpetas**:
   - Crea la carpeta `duplicados` si no existe.
   - Crea la carpeta `logs` si no existe.

2. **Limpieza Inicial**:
   - Si `duplicados` contiene archivos, estos se eliminan.

3. **Movimiento de Archivos**:
   - Compara archivos en `carpeta2` con archivos en `carpeta1` basándose en el nombre del archivo y el tamaño o hash (dependiendo del método de comparación seleccionado).
   - Mueve los archivos duplicados desde `carpeta2` a `duplicados`, manteniendo la estructura de carpetas desde la segunda carpeta en adelante.

4. **Eliminación de Carpetas Vacías**:
   - Después de mover los archivos, elimina las carpetas vacías en `carpeta2`.

5. **Registro de Logs**:
   - Guarda un registro detallado del proceso en un archivo dentro de la carpeta `logs`.
   - El archivo de log incluye la fecha y hora de ejecución, archivos movidos, tamaño de la carpeta `duplicados`, y el tiempo total del proceso.

## Requisitos

- Python 3.x
- Permisos de lectura y escritura en las carpetas `carpeta1`, `carpeta2`, `duplicados`, y `logs`.

## Uso

1. **Configuración**:
   - Asegúrate de que las carpetas `carpeta1`, `carpeta2`, `duplicados`, y `logs` estén configuradas correctamente y existan en el mismo directorio que el script, o ajusta las variables de configuración en el script.
   - Elige el método de comparación en el script. Puedes seleccionar entre:
     - `"rapido"`: Comparación basada en tamaño de archivo (más rápida).
     - `"hash"`: Comparación basada en hash SHA-256 (más precisa pero más lenta).

2. **Ejecución del Script**:
   - Ejecuta el script desde la línea de comandos con Python 3.x:
     ```bash
     python nombre_del_script.py
     ```

## Detalles del Script

### Variables de Configuración
```python
carpeta1 = "carpeta1"
carpeta2 = "carpeta2"
carpeta_duplicados = "duplicados"
carpeta_logs = "logs"
metodo_comparacion = "hash"  # Cambia a "rapido" si prefieres la comparación por tamaño
```
- `carpeta1` y `carpeta2`: Carpetas que se compararán para encontrar archivos duplicados.
- `carpeta_duplicados`: Carpeta donde se moverán los archivos duplicados.
- `carpeta_logs`: Carpeta donde se guardará el archivo de log.
- `metodo_comparacion`: Método de comparación a utilizar. `"rapido"` compara por tamaño, `"hash"` compara por hash SHA-256.

### Funciones del Script

- **`vaciar_carpeta(carpeta)`**:
  - Elimina todos los archivos y subcarpetas en la carpeta especificada.

- **`obtener_archivos(carpeta)`**:
  - Devuelve una lista de todas las rutas de archivos en la carpeta y sus subcarpetas.

- **`calcular_tamano_carpeta(carpeta)`**:
  - Calcula el tamaño total de todos los archivos en la carpeta.

- **`obtener_ruta_sin_dos_primeras(carpeta, archivo)`**:
  - Devuelve la ruta relativa de un archivo sin las dos primeras carpetas de la ruta.

- **`eliminar_carpetas_vacias(carpeta)`**:
  - Elimina las carpetas vacías dentro de la carpeta especificada.

- **`calcular_hash_archivo(archivo)`** (solo para método `"hash"`):
  - Calcula el hash SHA-256 de un archivo para comparación.

### Proceso del Script

1. **Configuración Inicial**:
   - Se configuran las rutas de las carpetas y el método de comparación.
   - Se crean las carpetas necesarias si no existen.

2. **Limpieza de Carpeta de Duplicados**:
   - Se vacía la carpeta `duplicados` si contiene archivos.

3. **Comparación y Movimiento de Archivos**:
   - Se obtienen todos los archivos de `carpeta1` y `carpeta2`.
   - Se crea un diccionario con las rutas de los archivos de `carpeta1`, ignorando las dos primeras carpetas.
   - Para cada archivo en `carpeta2`, se compara con los archivos en `carpeta1` (sin las dos primeras carpetas) utilizando el método de comparación seleccionado.
   - Los archivos duplicados se mueven a `duplicados` manteniendo la estructura de carpetas.

4. **Eliminación de Carpetas Vacías**:
   - Después de mover los archivos, se eliminan las carpetas vacías en `carpeta2`.

5. **Registro en Log**:
   - Se registra la fecha y hora de ejecución, los archivos movidos, el tamaño de la carpeta `duplicados`, y el tiempo total del proceso.

## Ejemplo de Salida del Log

```
Log de ejecución: 20240724_140500

Movido: carpeta2/carpetaazul/lua/entities/npc_vv_lion.lua a duplicados/lua/entities/npc_vv_lion.lua
Archivo duplicado encontrado en: carpeta1/otra_carpeta/lua/entities/npc_vv_lion.lua
-------------
Movido: carpeta2/anotherpath/file.txt a duplicados/anotherpath/file.txt
Archivo duplicado encontrado en: carpeta1/anotherpath/file.txt
-------------
Resumen del proceso:
Total de archivos movidos: 2
Tamaño total de la carpeta 'duplicados': 1.23 MB
Tiempo total del proceso: 5.67 segundos
```

## Notas

- Asegúrate de tener suficiente espacio en disco para la carpeta `duplicados`.
- Revisa los permisos de las carpetas para asegurar que el script pueda leer, escribir y eliminar archivos y carpetas.
- La opción `"hash"` proporciona una comparación más precisa pero puede ser más lenta que la opción `"rapido"`.

## Contribuciones

Si deseas contribuir al desarrollo de este script, por favor envía tus sugerencias o correcciones a través de un Pull Request o contacta al autor.
