from flask import request, jsonify

def listar_partidos():
    # TODO: Leer filtros (equipo, fecha, fase) y paginación (limit, offset)
    # TODO: Devolver paginación HATEOAS (first, prev, next, last)
    return jsonify({"mensaje": "Lista de partidos"}), 200

def crear_partido():
    # TODO: Leer body (equipo_local, equipo_visitante, fecha, fase)
    body = request.get_json()
    print(body)
    
    return jsonify({"mensaje": "Partido creado"}), 201

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