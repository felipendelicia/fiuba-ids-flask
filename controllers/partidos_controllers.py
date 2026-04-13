from flask import request, jsonify
from constants import FASES
from errors import ERRORS

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
    return jsonify({"mensaje": "Resultado actualizado"}), 200

def registrar_prediccion(id):
    # TODO: Validar que el partido no se haya jugado y que el usuario no tenga predicción
    # TODO: Leer body (id_usuario, local, visitante)
    return jsonify({"mensaje": "Predicción guardada"}), 201

def reemplazar_partido(id):
    return jsonify({"mensaje": "Partido reemplazado completo"}), 200

def actualizar_partido_parcial(id):
    return jsonify({"mensaje": "Partido actualizado parcialmente"}), 200