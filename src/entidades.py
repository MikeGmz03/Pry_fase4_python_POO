"""
Módulo de entidades base del sistema Software FJ.
Contiene la clase abstracta EntidadSistema y la clase concreta Cliente,
aplicando abstracción, herencia, encapsulación y validaciones estrictas.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import re

from src.excepciones import ErrorDatosInvalidos, ErrorParametroFaltante
from src.logger import logger


class EntidadSistema(ABC):
    """
    Clase abstracta que representa cualquier entidad general del sistema
    (Clientes, Servicios, Reservas). Garantiza una estructura común.
    """

    def __init__(self, id_entidad: str):
        # Validamos que el identificador no llegue vacío ni con espacios en blanco
        if not id_entidad or not isinstance(id_entidad, str) or not id_entidad.strip():
            raise ErrorParametroFaltante("El ID de la entidad es obligatorio y debe ser un texto válido.")

        # Atributos protegidos (encapsulación)
        self._id = id_entidad.strip()
        self._fecha_creacion = datetime.now()

    @property
    def id(self) -> str:
        """Retorna el identificador único de la entidad (solo lectura)."""
        return self._id

    @property
    def fecha_creacion(self) -> datetime:
        """Retorna la fecha y hora exacta en que se instanció la entidad."""
        return self._fecha_creacion

    @abstractmethod
    def validar(self) -> bool:
        """Método abstracto que obliga a las clases hijas a validar su estado interno."""
        pass

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto para devolver una representación legible de la entidad."""
        pass


class Cliente(EntidadSistema):
    """
    Representa a un cliente registrado en Software FJ.
    Encapsula sus datos personales y valida estrictamente cada asignación.
    """

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        # Inicializa el ID y la fecha de creación desde la clase padre
        super().__init__(id_cliente)

        # Atributos privados (doble guion bajo) gestionados vía setters con validación
        self.__nombre = ""
        self.__correo = ""
        self.__telefono = ""
        self.__activo = True

        # Se asignan usando las propiedades para disparar las validaciones desde el constructor
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

        # Validación integral final y registro en el archivo de logs
        self.validar()
        logger.info(f"Cliente creado exitosamente: {self.id} - {self.nombre}")

    @property
    def nombre(self) -> str:
        """Retorna el nombre completo del cliente."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        """Valida que el nombre no esté vacío y tenga una longitud mínima coherente."""
        if not valor or not isinstance(valor, str) or not valor.strip():
            raise ErrorParametroFaltante("El nombre del cliente es obligatorio.")
        if len(valor.strip()) < 3:
            raise ErrorDatosInvalidos(f"El nombre '{valor}' es demasiado corto (mínimo 3 caracteres).")
        self.__nombre = valor.strip()

    @property
    def correo(self) -> str:
        """Retorna el correo electrónico del cliente."""
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        """Valida el formato estándar de correo electrónico mediante expresión regular."""
        if not valor or not isinstance(valor, str) or not valor.strip():
            raise ErrorParametroFaltante("El correo electrónico del cliente es obligatorio.")
        patron_correo = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_correo, valor.strip()):
            raise ErrorDatosInvalidos(f"El correo '{valor}' no tiene un formato válido.")
        self.__correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        """Retorna el número telefónico del cliente."""
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        """Valida que el teléfono contenga únicamente dígitos y entre 7 y 15 caracteres."""
        if not valor or not isinstance(valor, str) or not valor.strip():
            raise ErrorParametroFaltante("El teléfono del cliente es obligatorio.")
        telefono_limpio = valor.strip()
        if not telefono_limpio.isdigit() or not (7 <= len(telefono_limpio) <= 15):
            raise ErrorDatosInvalidos(
                f"El teléfono '{valor}' es inválido. Debe contener solo dígitos (entre 7 y 15)."
            )
        self.__telefono = telefono_limpio

    @property
    def activo(self) -> bool:
        """Indica si el cliente está habilitado para realizar reservas."""
        return self.__activo

    def desactivar(self) -> None:
        """Desactiva al cliente sin eliminarlo de la memoria."""
        self.__activo = False
        logger.info(f"Cliente {self.id} ({self.nombre}) ha sido desactivado.")

    def validar(self) -> bool:
        """Verifica que todos los atributos obligatorios del cliente estén poblados."""
        if not all([self._id, self.__nombre, self.__correo, self.__telefono]):
            raise ErrorDatosInvalidos("El cliente posee datos incompletos o corruptos.")
        return True

    def obtener_resumen(self) -> str:
        """Devuelve un resumen formateado del cliente."""
        estado = "Activo" if self.__activo else "Inactivo"
        return f"Cliente [{self.id}] | {self.nombre} | {self.correo} | Tel: {self.telefono} | Estado: {estado}"

    def __str__(self) -> str:
        return self.obtener_resumen()