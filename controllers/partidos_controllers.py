from flask import request, jsonify
from constants import FASES
from errors import ERRORS
from db import execute
from helpers import build_links


def listar_partidos():
    # Leer filtros opcionales del query string
    equipo = request.args.get('equipo')
    fecha = request.args.get('fecha')
    fase = request.args.get('fase')

    # Validar fase si viene en el filtro
    if fase and fase not in FASES:
        return ERRORS["INVALID_FORMAT"]("La fase no es válida")

    # Leer parámetros de paginación (default: limit=10, offset=0)
    try:
        limit = int(request.args.get('_limit', 10))
        offset = int(request.args.get('_offset', 0))
    except ValueError:
        return ERRORS["INVALID_FORMAT"]("Los parámetros de paginación deben ser números enteros")

    if limit < 1 or offset < 0:
        return ERRORS["INVALID_FORMAT"]("Parámetros de paginación inválidos")

    # Construir cláusula WHERE con los filtros
    conditions = []
    if equipo:
        conditions.append(f"(equipo_local = '{equipo}' OR equipo_visitante = '{equipo}')")
    if fecha:
        conditions.append(f"fecha = '{fecha}'")
    if fase:
        conditions.append(f"fase = '{fase}'")

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    # Contar total de partidos para la paginación
    count_result = execute(f"SELECT COUNT(*) as total FROM partidos {where}")
    if count_result == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al contar partidos")

    total = count_result[0]['total']

    if total == 0:
        return '', 204

    # Traer partidos paginados (sin resultado, solo datos básicos)
    query = f"SELECT id, equipo_local, equipo_visitante, fecha, fase FROM partidos {where} LIMIT {limit} OFFSET {offset}"
    result = execute(query)
    if result == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al listar partidos")

    partidos = []
    for p in result:
        partidos.append({
            "id": p['id'],
            "equipo_local": p['equipo_local'],
            "equipo_visitante": p['equipo_visitante'],
            "fecha": str(p['fecha']),
            "fase": p['fase']
        })

    links = build_links(total, offset, limit)

    return jsonify({
        "partidos": partidos,
        "_links": links
    }), 200


def crear_partido():
    body = request.get_json()

    if not body:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("No mandaste el body")

    equipo_local = body.get('equipo_local')
    equipo_visitante = body.get('equipo_visitante')
    fecha = body.get('fecha')
    fase = body.get('fase')

    # Validar que todos los campos obligatorios estén presentes
    if not equipo_local or not equipo_visitante or not fecha or not fase:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("No mandaste los campos obligatorios para crear un partido")

    if equipo_local == equipo_visitante:
        return ERRORS["CONFLICT"]("Los equipos no pueden ser iguales")

    if fase not in FASES:
        return ERRORS["INVALID_FORMAT"]("La fase no es válida")

    query = f"INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase) VALUES ('{equipo_local}', '{equipo_visitante}', '{fecha}', '{fase}')"
    response = execute(query)

    if response == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al crear el partido")

    return '', 201


def obtener_partido(id):
    result = execute(f"SELECT * FROM partidos WHERE id = {id}")

    if result == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al obtener el partido")

    if len(result) == 0:
        return ERRORS["NOT_FOUND"](f"Partido con ID {id} no encontrado")

    p = result[0]

    # Incluir resultado solo si el partido ya se jugó (tiene goles cargados)
    resultado = None
    if p.get('goles_local') is not None:
        resultado = {
            "local": p['goles_local'],
            "visitante": p['goles_visitante']
        }

    return jsonify({
        "id": p['id'],
        "equipo_local": p['equipo_local'],
        "equipo_visitante": p['equipo_visitante'],
        "fecha": str(p['fecha']),
        "fase": p['fase'],
        "resultado": resultado
    }), 200


def eliminar_partido(id):
    # Verificar que el partido existe antes de intentar eliminarlo
    result = execute(f"SELECT id FROM partidos WHERE id = {id}")
    if result == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al buscar el partido")
    if len(result) == 0:
        return ERRORS["NOT_FOUND"](f"Partido con ID {id} no encontrado")

    # Borrar predicciones asociadas primero para no violar claves foráneas
    execute(f"DELETE FROM predicciones WHERE partido_id = {id}")

    response = execute(f"DELETE FROM partidos WHERE id = {id}")
    if response == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al eliminar el partido")

    return '', 204


def cargar_resultado(id):
    body = request.get_json()

    if not body:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("No mandaste el body")

    local = body.get('local')
    visitante = body.get('visitante')

    if local is None or visitante is None:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("Faltan los campos 'local' y 'visitante'")

    # Verificar que el partido existe
    result = execute(f"SELECT id FROM partidos WHERE id = {id}")
    if result == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al buscar el partido")
    if len(result) == 0:
        return ERRORS["NOT_FOUND"](f"Partido con ID {id} no encontrado")

    query = f"UPDATE partidos SET goles_local = {local}, goles_visitante = {visitante} WHERE id = {id}"
    response = execute(query)
    if response == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al cargar el resultado")

    return '', 204


def registrar_prediccion(id):
    body = request.get_json()

    if not body:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("No mandaste el body")

    id_usuario = body.get('id_usuario')
    local = body.get('local')
    visitante = body.get('visitante')

    if id_usuario is None or local is None or visitante is None:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("Faltan los campos obligatorios: id_usuario, local, visitante")

    # Verificar que el partido existe y que no se jugó todavía
    partido_result = execute(f"SELECT * FROM partidos WHERE id = {id}")
    if partido_result == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al buscar el partido")
    if len(partido_result) == 0:
        return ERRORS["NOT_FOUND"](f"Partido con ID {id} no encontrado")

    partido = partido_result[0]
    if partido.get('goles_local') is not None:
        # Si ya tiene resultado, no se puede predecir
        return ERRORS["CONFLICT"]("No se puede predecir un partido que ya se jugó")

    # Verificar que el usuario existe
    usuario_result = execute(f"SELECT id FROM usuarios WHERE id = {id_usuario}")
    if usuario_result == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al buscar el usuario")
    if len(usuario_result) == 0:
        return ERRORS["NOT_FOUND"](f"Usuario con ID {id_usuario} no encontrado")

    # Solo se permite una predicción por usuario por partido
    pred_result = execute(f"SELECT id FROM predicciones WHERE usuario_id = {id_usuario} AND partido_id = {id}")
    if pred_result == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al verificar predicciones existentes")
    if len(pred_result) != 0:
        return ERRORS["CONFLICT"]("Ya existe una predicción de este usuario para este partido")

    query = f"INSERT INTO predicciones (usuario_id, partido_id, goles_local, goles_visitante) VALUES ({id_usuario}, {id}, {local}, {visitante})"
    response = execute(query)
    if response == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al registrar la predicción")

    return '', 201


def reemplazar_partido(id):
    body = request.get_json()

    if not body:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("No mandaste el body")

    equipo_local = body.get('equipo_local')
    equipo_visitante = body.get('equipo_visitante')
    fecha = body.get('fecha')
    fase = body.get('fase')

    # Para PUT todos los campos son obligatorios
    if not equipo_local or not equipo_visitante or not fecha or not fase:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("Para reemplazar un partido se requieren todos los campos")

    if equipo_local == equipo_visitante:
        return ERRORS["CONFLICT"]("Los equipos no pueden ser iguales")

    if fase not in FASES:
        return ERRORS["INVALID_FORMAT"]("La fase no es válida")

    # Verificar que el partido existe
    result = execute(f"SELECT id FROM partidos WHERE id = {id}")
    if result == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al buscar el partido")
    if len(result) == 0:
        return ERRORS["NOT_FOUND"](f"Partido con ID {id} no encontrado")

    query = f"UPDATE partidos SET equipo_local = '{equipo_local}', equipo_visitante = '{equipo_visitante}', fecha = '{fecha}', fase = '{fase}' WHERE id = {id}"
    response = execute(query)
    if response == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al reemplazar el partido")

    return '', 204


def actualizar_partido_parcial(id):
    body = request.get_json()

    if not body:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("No mandaste ningún campo para actualizar")

    # Buscar el partido actual para comparar equipos si hace falta
    result = execute(f"SELECT * FROM partidos WHERE id = {id}")
    if result == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al buscar el partido")
    if len(result) == 0:
        return ERRORS["NOT_FOUND"](f"Partido con ID {id} no encontrado")

    partido_actual = result[0]

    # Validar fase si viene en el body
    if 'fase' in body and body['fase'] not in FASES:
        return ERRORS["INVALID_FORMAT"]("La fase no es válida")

    # Validar que los equipos no queden iguales después del update
    if 'equipo_local' in body or 'equipo_visitante' in body:
        equipo_local_final = body.get('equipo_local') or partido_actual['equipo_local']
        equipo_visitante_final = body.get('equipo_visitante') or partido_actual['equipo_visitante']
        if equipo_local_final == equipo_visitante_final:
            return ERRORS["CONFLICT"]("Los equipos no pueden ser iguales")

    # Construir la parte SET del UPDATE con solo los campos recibidos
    campos_validos = ['equipo_local', 'equipo_visitante', 'fecha', 'fase']
    update_parts = []
    for campo in campos_validos:
        if campo in body:
            update_parts.append(f"{campo} = '{body[campo]}'")

    if not update_parts:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("No mandaste ningún campo válido para actualizar")

    query = f"UPDATE partidos SET {', '.join(update_parts)} WHERE id = {id}"
    response = execute(query)
    if response == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al actualizar el partido")

    return '', 204
