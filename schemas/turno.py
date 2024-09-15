def turno_helper(turno) -> dict:
    # Convertimos la fecha y hora a formato específico
    fecha_formateada = turno["fecha"].strftime("%d-%m-%Y")
    
    # Verifica si 'hora' está en el diccionario y formatea
    hora_formateada = turno["hora"]  # Hora ya es una cadena en el formato deseado

    return {
        "id": str(turno["_id"]),
        "cliente_id": turno["cliente_id"],
        "fecha": fecha_formateada,
        "hora": hora_formateada,
        "servicio": turno["servicio"],
        "estado": turno["estado"],
        "notas": turno.get("notas", "")
    }