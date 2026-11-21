# 🚀 Software FJ — Sistema Integral de Gestión de Clientes, Servicios y Reservas

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Paradigma](https://img.shields.io/badge/Paradigma-POO-2EA44F?style=for-the-badge)
![Almacenamiento](https://img.shields.io/badge/Almacenamiento-En%20Memoria%20%2B%20Logs-F59E0B?style=for-the-badge)
![UNAD](https://img.shields.io/badge/UNAD-Programaci%C3%B3n%20213023-005883?style=for-the-badge)

Aplicación modular orientada a objetos desarrollada en **Python** para la empresa **Software FJ**, orientada a gestionar clientes, catálogo de servicios (reserva de salas, alquiler de equipos y asesorías especializadas) y el ciclo de vida completo de reservas **sin utilizar motores de bases de datos**. Toda la operación se administra en memoria mediante estructuras de objetos y listas internas, garantizando estabilidad continua mediante manejo avanzado de excepciones y registro persistente en archivos de *logs*.

---

## 📋 Contexto Académico

* **Institución:** Universidad Nacional Abierta y a Distancia (UNAD) — ECBTI
* **Programa:** Ingeniería de Sistemas
* **Curso:** Programación (Código `213023`)
* **Actividad:** Fase 4 — Componente Práctico (Prácticas Simuladas)

---

## 🧠 Principios de POO y Manejo de Excepciones Implementados

| Pilar / Requisito | Implementación en el Proyecto | Módulo |
| :--- | :--- | :--- |
| **Abstracción** | Clases abstractas `EntidadSistema` y `Servicio` (`abc.ABC`, `@abstractmethod`). | `src/entidades.py`, `src/servicios.py` |
| **Encapsulación** | Atributos protegidos (`_`) y privados (`__`) con validaciones estrictas mediante `@property` y *setters*. | `src/entidades.py`, `src/reservas.py` |
| **Herencia y Polimorfismo** | `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada` heredan de `Servicio` y sobrescriben `calcular_costo()`, `describir_servicio()` y `validar_parametros()`. | `src/servicios.py` |
| **Sobrecarga de Métodos** | Variantes de `calcular_costo(duracion, impuesto=0.0, descuento=0.0)` con parámetros opcionales y validación financiera. | `src/servicios.py` |
| **Excepciones Personalizadas** | Jerarquía propia heredada de `ErrorSoftwareFJ` con códigos internos (`ErrorDatosInvalidos`, `ErrorParametroFaltante`, `ErrorOperacionNoPermitida`, `ErrorServicioNoDisponible`, `ErrorReservaInvalida`, `ErrorCalculoInconsistente`). | `src/excepciones.py` |
| **Control de Flujo de Errores** | Uso explícito de `try/except` (`cancelar`), `try/except/else` (`confirmar`), `try/except/finally` (`procesar`) y **encadenamiento de excepciones** (`raise ... from e`). | `src/reservas.py`, `main.py` |
| **Auditoría y Logs** | Registro automático de eventos `INFO`, advertencias `WARNING` y errores `ERROR/CRITICAL` en `logs/sistema_fj.log`. | `src/logger.py` |

---

## 📂 Arquitectura del Proyecto

```text
Pry_fase4_python_POO/
├── src/
│   ├── __init__.py          # Inicialización del paquete fuente
│   ├── excepciones.py       # Jerarquía de excepciones personalizadas
│   ├── logger.py            # Configuración del archivo de logs (archivo + consola)
│   ├── entidades.py         # Clase abstracta EntidadSistema y clase Cliente
│   ├── servicios.py         # Clase abstracta Servicio y 3 servicios especializados
│   ├── reservas.py          # Clase Reserva (estados, validaciones y encadenamiento)
│   └── sistema.py           # Orquestador SistemaGestionFJ (listas en memoria)
├── logs/
│   ├── .gitkeep             # Mantiene la carpeta versionada en Git
│   └── sistema_fj.log       # Generado automáticamente en ejecución (ignorado por Git)
├── main.py                  # Simulación integral de 12 operaciones (exitosas y fallidas)
├── .gitignore
└── README.md
```

---

## ⚙️ Instalación y Ejecución

No requiere librerías externas; funciona íntegramente con la biblioteca estándar de **Python 3.10+**.

### 1. Clonar el repositorio
```bash
git clone git@github.com:MikeGmz03/Pry_fase4_python_POO.git
cd Pry_fase4_python_POO
```

### 2. Ejecutar la simulación
```bash
python3 main.py
```

### 3. Consultar el archivo de auditoría (*logs*)
```bash
cat logs/sistema_fj.log
```

---

## 🧪 Simulación de Operaciones (`main.py`)

El script principal ejecuta **12 operaciones controladas** (superando el mínimo de 10 requeridas) demostrando tolerancia a fallos sin interrumpir la ejecución:

1. Registro válido de Cliente 1 (`Ana Pérez`).
2. Registro válido de Cliente 2 (`Carlos Gómez`).
3. Registro inválido de cliente por correo electrónico mal formado (`ErrorDatosInvalidos`).
4. Registro inválido de cliente por parámetro faltante en teléfono (`ErrorParametroFaltante`).
5. Creación válida de los 3 servicios polimórficos (Sala, Equipo y Asesoría).
6. Creación inválida de servicio por tarifa negativa (`ErrorDatosInvalidos`).
7. Reserva exitosa de sala: confirmación y procesamiento con IVA (19%) y descuento (10%).
8. Reserva exitosa de asesoría Senior: confirmación y procesamiento con IVA (19%).
9. Reserva fallida por duración fuera de rango con **encadenamiento de excepciones** (`ErrorReservaInvalida` ← `ErrorDatosInvalidos`).
10. Procesamiento fallido por descuento inconsistente (95%) con **encadenamiento de excepciones** (`ErrorReservaInvalida` ← `ErrorCalculoInconsistente`).
11. Cancelación exitosa de reserva y bloqueo de doble cancelación (`ErrorOperacionNoPermitida`).
12. Intento fallido de reserva sobre un servicio marcado como no disponible (`ErrorServicioNoDisponible`).

Al finalizar, el sistema imprime el **Reporte Final en Memoria** comprobando la integridad de los datos válidos.

---

## 🤝 Flujo Colaborativo en Git

Para mantener el repositorio organizado entre los integrantes del equipo:

```bash
# 1. Actualizar la rama principal antes de trabajar
git checkout main
git pull origin main

# 2. Crear una rama para tu mejora o ajuste
git checkout -b feat/nombre-de-tu-aporte

# 3. Guardar y subir cambios
git add .
git commit -m "feat: descripción clara del cambio"
git push origin feat/nombre-de-tu-aporte
```

---

## 👥 Equipo de Desarrollo

| Integrante | Usuario GitHub | Rol / Aporte Principal |
| :--- | :--- | :--- |
| **Michael Steven Gómez Giraldo** | [@MikeGmz03](https://github.com/MikeGmz03) | Configuración del repositorio, arquitectura POO y módulos base |
| *Integrante 2* | `@usuario2` | *Validaciones / Pruebas / Documentación* |
| *Integrante 3* | `@usuario3` | *Validaciones / Pruebas / Documentación* |
| *Integrante 4* | `@usuario4` | *Validaciones / Pruebas / Documentación* |
| *Integrante 5* | `@usuario5` | *Validaciones / Pruebas / Documentación* |

---

## 📚 Referencias

* Cuevas Álvarez, A. (2016). *Python 3: curso práctico*. RA-MA Editorial.
* Romano, F., Baka, B., & Phillips, D. (2019). *Getting Started with Python: Understand Key Data Structures and Use Python in Object-oriented Programming*. Packt Publishing.
* Van Rossum, G., & Drake Jr, F. L. (2024). *El tutorial de Python: Errores y excepciones*. Python Software Foundation. https://docs.python.org/es/3.12/tutorial/errors.html
