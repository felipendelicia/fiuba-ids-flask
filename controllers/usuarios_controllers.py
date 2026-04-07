from flask import request, jsonify

def crear_usuario():
    # TODO: Leer body (nombre, email). No requiere auth 
    return jsonify({"mensaje": "Usuario creado"}), 201

def listar_usuarios():
    # TODO: Soportar paginación (limit, offset) 
    return jsonify({"mensaje": "Lista de usuarios"}), 200

def obtener_usuario(id):
    # TODO: Buscar usuario por ID 
    return jsonify({"mensaje": f"Detalle usuario {id}"}), 200

def reemplazar_usuario(id):
    # TODO: Reemplazar datos del usuario
    return jsonify({"mensaje": "Usuario reemplazado"}), 200

def eliminar_usuario(id):
    # TODO: Eliminar usuario por ID
    return '', 204