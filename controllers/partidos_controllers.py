from flask import request, jsonify
from constants import FASES
from errors import ERRORS

from controllers.usuarios_controllers import obtener_usuario

from db import execute

def listar_partidos():
    # TODO: Leer filtros (equipo, fecha, fase) y paginación (limit, offset)
    # TODO: Devolver paginación HATEOAS (first, prev, next, last)
    return jsonify({"mensaje": "Lista de partidos"}), 200

def crear_partido():
    # TODO: Leer body (equipo_local, equipo_visitante, fecha, fase)
    body = request.get_json()

    if body.get('equipo_local') == None or body.get('equipo_visitante') == None or body.get('fecha') == None or body.get('fase') == None:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("No mandaste los campos obligatorios para crear un partido")
    
    if body.get('equipo_local') == body.get('equipo_visitante'):
        return ERRORS["CONFLICT"]("Los equipos no pueden ser iguales")
    
    if body.get('fase') not in FASES:
        return ERRORS["INVALID_FORMAT"]("La fase no es válida")
    
    query = f"INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase) VALUES ('{body.get('equipo_local')}', '{body.get('equipo_visitante')}', '{body.get('fecha')}', '{body.get('fase')}')"

    response = execute(query)

    if response == False: return ERRORS["UNKNOWN_ERROR"]("Error al crear el partido")
    
    return "", 201

def obtener_partido(id):
    # TODO: Buscar partido por ID en DB e incluir el resultado si existe 
    return jsonify({"mensaje": f"Detalle del partido {id}"}), 200

def eliminar_partido(id):
    # TODO: Borrar partido de la DB 
    return '', 204

def cargar_resultado(id):
    # TODO: Leer body (goles_local, goles_visitante) y actualizar DB 
    body = request.get_json()

    if body.get('goles_local') == None or body.get('goles_visitante') == None:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("No mandaste los campos obligatorios para cargar/actualizar el resultado")
    partido_response = obtener_partido(id)
    if partido_response[1] != 200:
        return partido_response
    
    query = f"UPDATE partidos SET goles_local = {body.get('goles_local')}, goles_visitante = {body.get('goles_visitante')} WHERE id = {id}"

    response = execute(query)

    if response == False: return ERRORS["UNKNOWN_ERROR"]("Error al actualizar el resultado")

    return jsonify({"mensaje": "Resultado actualizado"}), 200

def registrar_prediccion(id:int):
    # TODO: Validar que el partido no se haya jugado y que el usuario no tenga predicción
    # TODO: Leer body (id_usuario, local, visitante)

    body = request.get_json()

    if body.get('id_usuario') == None or body.get('local') == None or body.get('visitante') == None:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("No mandaste los campos obligatorios para crear una prediccion")

    partido_response = obtener_partido(id)
    usuario_response = obtener_usuario(body.get('id_usuario'))

    # Reviso que las entradas del partido y usuario esten OK y existan.
    if partido_response[1] != 200:
        return partido_response
    
    if usuario_response[1] != 200:
        return usuario_response
    
    # Reviso que la prediccion sea unica para ese usuario.
    query = f"SELECT * FROM predicciones WHERE usuario_id = {body.get('id_usuario')} AND partido_id = {id}"

    response = execute(query)

    if response == False: return ERRORS["UNKNOWN_ERROR"]("Error al obtener predicciones")

    if len(response) != 0: return ERRORS["CONFLICT"]("Ya tienes una predicción para este partido")

    query = f"INSERT INTO predicciones (usuario_id, partido_id, goles_local, goles_visitante) VALUES ({body.get("id_usuario")}, {id}, {body.get("goles_local")}, {body.get("goles_visitante")})"

    response = execute(query)

    if response == False: return ERRORS["UNKNOWN_ERROR"]("Error al insertar nueva predicción")

    return "", 201

def reemplazar_partido(id):
    return jsonify({"mensaje": "Partido reemplazado completo"}), 200

def actualizar_partido_parcial(id):
    body = request.get_json()
    
    campos_validos = ['equipo_local', 'equipo_visitante', 'fecha', 'fase']
    update = []

    if not body:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("No mandaste ningún campo para actualizar el partido")

    partido_response = obtener_partido(id)
    if partido_response[1] != 200:
        return partido_response
    
    if "fase" in body and body["fase"] not in FASES:
        return ERRORS["INVALID_FORMAT"]("La fase no es válida")

    # verifico que los campos a actualizar sean válidos y los agrego a la query de update
    if "equipo_local" in body or "equipo_visitante" in body:

        equipo_local_final = body.get("equipo_local") if body.get("equipo_local") else partido_response[0].get("equipo_local")
        equipo_visitante_final = body.get("equipo_visitante") if body.get("equipo_visitante") else partido_response[0].get("equipo_visitante")
        if equipo_local_final == equipo_visitante_final:
            return ERRORS["CONFLICT"]("Los equipos no pueden ser iguales")
    
    for campo in campos_validos:
        if campo in body:
            update.append(f"{campo} = '{body[campo]}'")
    
    if len(update) == 0:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("No mandaste ningún campo para actualizar el partido")
    
    query = f"UPDATE partidos SET {', '.join(update)} WHERE id = {id}"

    response = execute(query)

    if response == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al actualizar el partido")
    
    return "", 204
