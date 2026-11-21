"""
Punto de entrada principal del Sistema Integral de Gestión de Software FJ.
Simula 12 operaciones completas (exitosas y fallidas) para demostrar
polimorfismo, sobrecarga, encapsulación, manejo avanzado de excepciones
y continuidad operativa sin uso de bases de datos.
"""

from src.entidades import Cliente
from src.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from src.sistema import SistemaGestionFJ
from src.excepciones import ErrorSoftwareFJ
from src.logger import logger


def ejecutar_operacion(numero: int, descripcion: str, funcion):
    """
    Wrapper seguro que ejecuta cada operación de la simulación,
    captura cualquier excepción controlada y evita que la aplicación se detenga.
    """
    print(f"\n--- Operación {numero:02d}: {descripcion} ---")
    try:
        resultado = funcion()
        print(f"[OK] Operación completada con éxito.")
        return resultado
    except ErrorSoftwareFJ as e:
        print(f"[ERROR CONTROLADO] {e}")
        # Muestra la causa original si hubo encadenamiento de excepciones
        if e.__cause__:
            print(f"   ↳ Causa encadenada: {e.__cause__}")
        logger.warning(f"Operación {numero:02d} controlada tras error: {e}")
    except Exception as e:
        print(f"[ERROR INESPERADO CONTROLADO] {e}")
        logger.critical(f"Error inesperado en operación {numero:02d}: {e}")
    return None


def main():
    sistema = SistemaGestionFJ()
    print("=== INICIANDO SIMULACIÓN DE OPERACIONES - SOFTWARE FJ ===")

    # 1. Registro válido de Cliente 1
    ejecutar_operacion(1, "Registrar cliente válido (Ana Pérez)", lambda: (
        sistema.registrar_cliente(Cliente("CLI-01", "Ana Pérez", "ana.perez@correo.com", "3001234567"))
    ))

    # 2. Registro válido de Cliente 2
    ejecutar_operacion(2, "Registrar cliente válido (Carlos Gómez)", lambda: (
        sistema.registrar_cliente(Cliente("CLI-02", "Carlos Gómez", "carlos.g@empresa.co", "3109876543"))
    ))

    # 3. Registro INVÁLIDO de Cliente (correo mal formado)
    ejecutar_operacion(3, "Intentar registrar cliente con correo inválido", lambda: (
        sistema.registrar_cliente(Cliente("CLI-03", "Luis Mora", "correo_invalido_sin_arroba", "3001112233"))
    ))

    # 4. Registro INVÁLIDO de Cliente (parámetro faltante)
    ejecutar_operacion(4, "Intentar registrar cliente sin teléfono", lambda: (
        sistema.registrar_cliente(Cliente("CLI-04", "Marta Ruiz", "marta@correo.com", ""))
    ))

    # 5. Creación válida de 3 servicios polimórficos (Sala, Equipo, Asesoría)
    def crear_servicios_validos():
        sistema.registrar_servicio(ReservaSala("SRV-01", "Sala Innovación", 85000, capacidad=20, tiene_proyector=True))
        sistema.registrar_servicio(AlquilerEquipo("SRV-02", "Kit Portátiles Dev", 45000, tipo_equipo="Laptop i7", cantidad=3))
        sistema.registrar_servicio(AsesoriaEspecializada("SRV-03", "Consultoría Cloud", 150000, especialidad="GCP", nivel_senior=True))

    ejecutar_operacion(5, "Crear 3 servicios válidos (Sala, Equipo y Asesoría)", crear_servicios_validos)

    # 6. Creación INVÁLIDA de servicio (tarifa negativa)
    ejecutar_operacion(6, "Intentar crear servicio con tarifa negativa", lambda: (
        sistema.registrar_servicio(ReservaSala("SRV-04", "Sala Error", -50000, capacidad=10))
    ))

    # 7. Reserva EXITOSA de Sala (confirmada y procesada con IVA 19% y descuento 10%)
    def reserva_exitosa_sala():
        r = sistema.crear_reserva("RES-01", "CLI-01", "SRV-01", duracion=4)
        r.confirmar()
        costo = r.procesar(impuesto=0.19, descuento=0.10)
        print(f"   -> {r.obtener_resumen()} (Costo: ${costo:,.2f})")

    ejecutar_operacion(7, "Reserva completa exitosa de Sala (con IVA y descuento)", reserva_exitosa_sala)

    # 8. Reserva EXITOSA de Asesoría Senior (confirmada y procesada solo con IVA)
    def reserva_exitosa_asesoria():
        r = sistema.crear_reserva("RES-02", "CLI-02", "SRV-03", duracion=2.5)
        r.confirmar()
        costo = r.procesar(impuesto=0.19)
        print(f"   -> {r.obtener_resumen()} (Costo: ${costo:,.2f})")

    ejecutar_operacion(8, "Reserva completa exitosa de Asesoría Senior", reserva_exitosa_asesoria)

    # 9. Reserva FALLIDA por duración inválida (demuestra encadenamiento de excepciones)
    ejecutar_operacion(9, "Intentar reservar sala por 20 horas (excede máximo de 12h)", lambda: (
        sistema.crear_reserva("RES-03", "CLI-01", "SRV-01", duracion=20)
    ))

    # 10. Reserva FALLIDA por cálculo inconsistente (descuento > 80% -> encadenamiento)
    def reserva_fallo_calculo():
        r = sistema.crear_reserva("RES-04", "CLI-02", "SRV-02", duracion=5)
        r.confirmar()
        r.procesar(impuesto=0.19, descuento=0.95)  # Descuento inválido

    ejecutar_operacion(10, "Intentar procesar reserva con descuento inconsistente (95%)", reserva_fallo_calculo)

    # 11. Cancelación exitosa e intento fallido de cancelar una reserva ya procesada
    def prueba_cancelacion():
        r_cancel = sistema.crear_reserva("RES-05", "CLI-01", "SRV-02", duracion=2)
        r_cancel.cancelar(motivo="Cambio de agenda del cliente")
        print(f"   -> {r_cancel.obtener_resumen()}")
        # Intentamos cancelar la misma reserva de nuevo (debe fallar controladamente)
        r_cancel.cancelar(motivo="Segundo intento")

    ejecutar_operacion(11, "Cancelar reserva y probar doble cancelación no permitida", prueba_cancelacion)

    # 12. Reserva FALLIDA por servicio no disponible
    def reserva_servicio_no_disponible():
        srv = sistema.buscar_servicio("SRV-02")
        srv.disponible = False
        sistema.crear_reserva("RES-06", "CLI-01", "SRV-02", duracion=3)

    ejecutar_operacion(12, "Intentar reservar un servicio marcado como no disponible", reserva_servicio_no_disponible)

    # Reporte final demostrando que la aplicación terminó íntegra y sin caídas
    print(sistema.generar_reporte())
    logger.info("=== Simulación de 12 operaciones finalizada sin interrupciones ===")


if __name__ == "__main__":
    main()