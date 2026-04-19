from flask import request, jsonify
from db import execute
from errors import ERRORS
from helpers import build_links


def crear_usuario():
    data = request.get_json()

    if not data:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("No mandaste el body")

    nombre = data.get("nombre")
    email = data.get("email")

    if not nombre or not email:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("Nombre y email son requeridos")

    # Verificar que el email no esté ya registrado
    result = execute(f"SELECT id FROM usuarios WHERE email = '{email}'")
    if result == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al verificar el email")
    if len(result) != 0:
        return ERRORS["CONFLICT"]("El email ya está registrado")

    response = execute(f"INSERT INTO usuarios (nombre, email) VALUES ('{nombre}', '{email}')")
    if response == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al crear el usuario")

    return '', 201


def listar_usuarios():
    # Leer parámetros de paginación
    try:
        limit = int(request.args.get('_limit', 10))
        offset = int(request.args.get('_offset', 0))
    except ValueError:
        return ERRORS["INVALID_FORMAT"]("Los parámetros de paginación deben ser enteros")

    if limit < 1 or offset < 0:
        return ERRORS["INVALID_FORMAT"]("Parámetros de paginación inválidos")

    # Contar total para calcular los links
    count_result = execute("SELECT COUNT(*) as total FROM usuarios")
    if count_result == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al contar usuarios")

    total = count_result[0]['total']

    if total == 0:
        return '', 204

    result = execute(f"SELECT id, nombre FROM usuarios LIMIT {limit} OFFSET {offset}")
    if result == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al listar usuarios")

    # El swagger muestra solo id y nombre en el listado (no email)
    usuarios = [{"id": u['id'], "nombre": u['nombre']} for u in result]
    links = build_links(total, offset, limit)

    return jsonify({
        "usuarios": usuarios,
        "_links": links
    }), 200


def obtener_usuario(id):
    result = execute(f"SELECT * FROM usuarios WHERE id = {id}")

    if result == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al obtener el usuario")

    if len(result) == 0:
        return ERRORS["NOT_FOUND"](f"Usuario con ID {id} no encontrado")

    u = result[0]
    return jsonify({
        "id": u['id'],
        "nombre": u['nombre'],
        "email": u['email']
    }), 200


def reemplazar_usuario(id):
    body = request.get_json()

    if not body:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("No mandaste el body")

    nombre = body.get("nombre")
    email = body.get("email")

    if not nombre or not email:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("Nombre y email son requeridos")

    # Verificar que el usuario existe
    result = execute(f"SELECT id FROM usuarios WHERE id = {id}")
    if result == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al buscar el usuario")
    if len(result) == 0:
        return ERRORS["NOT_FOUND"](f"Usuario con ID {id} no encontrado")

    # Verificar que el email no lo use otro usuario
    result = execute(f"SELECT id FROM usuarios WHERE email = '{email}' AND id != {id}")
    if result == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al verificar el email")
    if len(result) != 0:
        return ERRORS["CONFLICT"]("El email ya está registrado en otro usuario")

    response = execute(f"UPDATE usuarios SET nombre = '{nombre}', email = '{email}' WHERE id = {id}")
    if response == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al actualizar el usuario")

    return '', 204


def eliminar_usuario(id):
    # Verificar que el usuario existe
    result = execute(f"SELECT id FROM usuarios WHERE id = {id}")
    if result == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al buscar el usuario")
    if len(result) == 0:
        return ERRORS["NOT_FOUND"](f"Usuario con ID {id} no encontrado")

    # Borrar predicciones del usuario antes de eliminarlo
    execute(f"DELETE FROM predicciones WHERE usuario_id = {id}")

    response = execute(f"DELETE FROM usuarios WHERE id = {id}")
    if response == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al eliminar el usuario")

    return '', 204
