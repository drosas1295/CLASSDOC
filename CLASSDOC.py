

# Importar las bibliotecas necesarias
import os  # Para operaciones del sistema operativo
import pandas as pd  # Para manipulación y análisis de datos
import shutil  # Para operaciones de archivos y carpetas
import datetime  # Para manejar fechas y tiempos
import sys # Para importar el sistema
# Configurar opciones de visualización de Pandas
pd.set_option('display.max_columns', None)  # Mostrar todas las columnas en la salida
pd.set_option('display.max_rows', None)  # Mostrar todas las filas en la salida
pd.set_option('display.width', None)  # No truncar la salida en ancho
pd.set_option('display.max_colwidth', None)  # No truncar el contenido de las celdas

# Definir los directorios de entrada y salida
directorio_raiz = 'D:/UNIVERSIDAD 2023-2/ALGORITMOS Y PROGRAMACION/ENTREGA 2/TrabajoFinal/tmp'
directorio_salida = 'D:/UNIVERSIDAD 2023-2/ALGORITMOS Y PROGRAMACION/ENTREGA 2/TrabajoFinal/orden'

# Función para obtener el tipo de archivo a partir del nombre
def obtener_tipo_archivo(archivo):
    # Divide el nombre del archivo y su extensión
    nombre, extension = os.path.splitext(archivo)
    return extension

# Función para contar las vocales en el nombre del archivo
def contar_vocales(nombre):
    # Definir las vocales en mayúsculas y minúsculas
    vocales = "AEIOUaeiou"
    # Contar el número de vocales en el nombre
    return sum(1 for letra in nombre if letra in vocales)

# Función para contar las consonantes en el nombre del archivo
def contar_consonantes(nombre):
    # Definir las consonantes en mayúsculas y minúsculas
    consonantes = "BCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz"
    # Contar el número de consonantes en el nombre
    return sum(1 for letra in nombre if letra in consonantes)

# Crear un DataFrame para almacenar la información de cada archivo
columnas = ['Nombre Anterior', 'Nombre Actual', 'Ruta Anterior', 'Nueva Ruta', 'Tipo de Archivo', 'Tamaño (bit)', 'Tamaño (byte)', 'Tamaño (Kilobyte)', 'Tamaño (Megabyte)', 'Vocales', 'Consonantes', 'Fecha de Creación', 'Última Fecha de Modificación', 'Cantidad de Archivos del Mismo Tipo']
df = pd.DataFrame(columns=columnas)

# Registro de eventos para mantener un seguimiento de las acciones realizadas
log = []
log.append(f'Daniel Rosas , sistema operativo {os.name}, plataforma {sys.platform}, fecha {datetime.datetime.now().strftime("%Y%m%d%H%M%S")}')
log.append('"CLASSDOC" pretende revolucionar la forma en que las personas y las organizaciones gestionan sus activos digitales.')
def registrar_evento(evento):
    # Registrar el evento con la marca de tiempo y el tiempo transcurrido
    ahora = datetime.datetime.now()
    log.append(f"{ahora}\t{evento}\tTiempo empleado: {str(datetime.datetime.now() - inicio)}")

# Iniciar el tiempo
inicio = datetime.datetime.now()

# Crear directorios para los tipos de archivos
tipos_de_archivo = set()

# Obtener todos los tipos de archivos presentes en el directorio raíz
for raiz, directorios, archivos in os.walk(directorio_raiz):
    for archivo in archivos:
        ruta_completa = os.path.join(raiz, archivo)
        tipo_archivo = obtener_tipo_archivo(archivo)
        tipos_de_archivo.add(tipo_archivo)

# Crear directorios para organizar los archivos según su tipo
for tipo in tipos_de_archivo:
    directorio_tipo = os.path.join(directorio_salida, tipo.strip('.'))
    
    # Cambiar nombres de carpetas según la extensión
    if tipo == '.xlsx':
        directorio_tipo = os.path.join(directorio_salida, 'excel')
    elif tipo == '.docx':
        directorio_tipo = os.path.join(directorio_salida, 'word')
    elif tipo == '.pptx':
        directorio_tipo = os.path.join(directorio_salida, 'powerpoint')
    
    os.makedirs(directorio_tipo, exist_ok=True)  # Crear directorios si no existen

# Recorrer nuevamente el árbol de directorios y organizar los archivos
for raiz, directorios, archivos in os.walk(directorio_raiz):
    for archivo in archivos:
        ruta_completa = os.path.join(raiz, archivo)
        tipo_archivo = obtener_tipo_archivo(archivo)
        directorio_tipo = os.path.join(directorio_salida, tipo_archivo.strip('.'))
        
        # Cambiar nombres de carpetas según la extensión
        if tipo_archivo == '.xlsx':
            directorio_tipo = os.path.join(directorio_salida, 'excel')
        elif tipo_archivo == '.docx':
            directorio_tipo = os.path.join(directorio_salida, 'word')
        elif tipo_archivo == '.pptx':
            directorio_tipo = os.path.join(directorio_salida, 'powerpoint')
        
        # Copiar el archivo al directorio correspondiente y renombrarlo
        nuevo_nombre = f"{len(os.listdir(directorio_tipo)) + 1:03d}-{archivo}"
        nueva_ruta = os.path.join(directorio_tipo, nuevo_nombre)
        shutil.copy(ruta_completa, nueva_ruta)

        # Estadísticas del archivo
        estatisticas_archivo = [archivo, nuevo_nombre, raiz, nueva_ruta, tipo_archivo]
        tamaño = os.path.getsize(nueva_ruta)
        estatisticas_archivo.extend([tamaño, tamaño / 8, tamaño / 8 / 1024, tamaño / 8 / 1024 / 1024])
        estatisticas_archivo.append(contar_vocales(archivo))
        estatisticas_archivo.append(contar_consonantes(archivo))
        estatisticas_archivo.append(datetime.datetime.fromtimestamp(os.path.getctime(nueva_ruta)))
        estatisticas_archivo.append(datetime.datetime.fromtimestamp(os.path.getmtime(nueva_ruta)))

        # Contar la cantidad de archivos del mismo tipo
        cantidad_archivos_mismo_tipo = len(os.listdir(directorio_tipo))
        estatisticas_archivo.append(cantidad_archivos_mismo_tipo)
        
        df.loc[len(df)] = estatisticas_archivo
        
        evento = f"Mover {archivo} a {nuevo_nombre}"
        registrar_evento(evento)

# Guardar el DataFrame en un archivo Excel en el directorio de salida
ruta_resultado_excel = os.path.join(directorio_salida, 'archivo_resultado.xlsx') 
# Verificar si el archivo ya existe
if os.path.exists(ruta_resultado_excel):
    # Si existe, intenta eliminarlo
    try:
        os.remove(ruta_resultado_excel)
    except Exception as e:
        print(f"No se pudo eliminar el archivo existente: {e}")

# Guardar el DataFrame en el nuevo archivo Excel
df.to_excel(ruta_resultado_excel, index=False)

# Mostrar el DataFrame en la consola
print(df)

# Guardar el registro de eventos en un archivo de texto en el directorio de salida
ruta_registro_eventos = os.path.join(directorio_salida, 'registro_eventos.txt')
with open(ruta_registro_eventos, 'w') as archivo_log:
    for evento in log:
        archivo_log.write(evento + '\n')

# Finalizar el tiempo y registrar evento
fin = datetime.datetime.now()
registrar_evento(f"Procedimiento completado. Total de procedimientos realizados: {len(log)}")

print("Proceso completado")
