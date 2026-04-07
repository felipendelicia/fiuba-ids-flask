from flask import request, jsonify

def obtener_ranking():
    # TODO: Soportar paginación (limit, offset) 
    # TODO: Calcular puntos (3 exacto, 1 correcto, 0 incorrecto)
    # TODO: Devolver lista con id_usuario y puntos
    return jsonify({"mensaje": "Ranking calculado"}), 200