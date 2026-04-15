from flask import request, jsonify
from db import execute
from errors import ERRORS


def crear_usuario():
    # TODO: Leer body (nombre, email). No requiere auth 
    data = request.get_json()
    
    #Obtener los campos
    nombre = data.get("nombre")
    email = data.get("email")
    
    #Validar campos obligatorios
    if not nombre or not email:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("Nombre y email son requeridos")
    
    #Verificar si el email ya existe
    query = f"SELECT * FROM usuarios WHERE email = '{email}'"
    response = execute(query)

    if response == False: return ERRORS["UNKNOWN_ERROR"]("Error al obtener usuarios")

    if len(response) != 0: return ERRORS["CONFLICT"]("Email ya registrado")
    
    #Insertar nuevo usuario
    query = f"INSERT INTO usuarios (nombre, email) VALUES ('{nombre}', '{email}')"
    response = execute(query)
    if response == False: return ERRORS["UNKNOWN_ERROR"]("Error al crear usuario")
    
    return "", 201
    
def listar_usuarios():
    # TODO: Soportar paginación (limit, offset) 
    return jsonify({"mensaje": "Lista de usuarios"}), 200

def obtener_usuario(id):
    # TODO: Buscar usuario por ID 
    return jsonify({"mensaje": f"Detalle usuario {id}"}), 200

def reemplazar_usuario(id):

    body = request.get_json()

    nombre = body.get("nombre")
    email = body.get("email")

    if not nombre or not email:
        return ERRORS["MISSING_REQUIRED_FIELDS"]("Nombre y email son requeridos")

    query = f"SELECT * FROM usuarios WHERE id = {id}"
    response = execute(query)

    if response == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al obtener usuarios")

    if len(response) == 0:
        return ERRORS["NOT_FOUND"](f"Usuario con ID {id} no encontrado")

    query = f"SELECT * FROM usuarios WHERE email = '{email}' AND id != {id}"
    response = execute(query)

    if response == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al verificar email")

    if len(response) != 0:
        return ERRORS["CONFLICT"]("Email ya registrado en otro usuario")

    query = f"UPDATE usuarios SET nombre = '{nombre}', email = '{email}' WHERE id = {id}"
    response = execute(query)

    if response == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al actualizar usuario")

    return "", 204

def eliminar_usuario(id):
    # TODO: Eliminar usuario por ID
    return '', 204