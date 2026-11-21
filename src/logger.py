"""
Módulo de configuración de logs para Software FJ.
Registra todos los eventos relevantes y errores en un archivo local
sin utilizar bases de datos.
"""

import logging
import os


def configurar_logger(nombre_logger: str = "SoftwareFJ", ruta_archivo: str = "logs/sistema_fj.log") -> logging.Logger:
    """
    Crea y configura una instancia de Logger que escribe en archivo y consola.

    Args:
        nombre_logger (str): Nombre identificador del logger.
        ruta_archivo (str): Ruta relativa del archivo donde se guardarán los logs.

    Returns:
        logging.Logger: Objeto logger listo para registrar eventos y errores.
    """
    # Garantiza que el directorio de logs exista antes de crear el archivo
    directorio = os.path.dirname(ruta_archivo)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio)

    logger = logging.getLogger(nombre_logger)
    logger.setLevel(logging.DEBUG)

    # Evita duplicar mensajes si la función se invoca desde varios módulos
    if not logger.handlers:
        # Formato estandarizado: Fecha/Hora | Nivel | Módulo | Mensaje
        formato = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(module)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Handler 1: Escritura persistente en archivo de texto (UTF-8)
        file_handler = logging.FileHandler(ruta_archivo, mode="a", encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formato)

        # Handler 2: Salida en consola para seguimiento durante la ejecución
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formato)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


# Instancia global compartida por todos los módulos del proyecto
logger = configurar_logger()