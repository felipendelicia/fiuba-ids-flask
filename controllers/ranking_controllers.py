from flask import request, jsonify
from db import execute
from errors import ERRORS
from helpers import build_links


def calcular_puntos(pred):
    marcador_exacto = pred['pred_local'] == pred['real_local'] and pred['pred_visitante'] == pred['real_visitante']
    mismo_ganador = (pred['pred_local'] > pred['pred_visitante']) == (pred['real_local'] > pred['real_visitante'])
    mismo_empate = pred['pred_local'] == pred['pred_visitante'] and pred['real_local'] == pred['real_visitante']

    if marcador_exacto:
        return 3
    if mismo_ganador or mismo_empate:
        return 1
    return 0


def construir_ranking(puntos_por_usuario):
    ranking = []
    for uid, pts in puntos_por_usuario.items():
        ranking.append({"id_usuario": uid, "puntos": pts})

    for i in range(len(ranking)):
        indice_mayor = i
        for j in range(i + 1, len(ranking)):
            if ranking[j]['puntos'] > ranking[indice_mayor]['puntos']:
                indice_mayor = j
        ranking[i], ranking[indice_mayor] = ranking[indice_mayor], ranking[i]

    return ranking


def obtener_ranking():
    try:
        limit = int(request.args.get('_limit', 10))
        offset = int(request.args.get('_offset', 0))
    except ValueError:
        return ERRORS["INVALID_FORMAT"]("Los parámetros de paginación deben ser enteros")

    if limit < 1 or offset < 0:
        return ERRORS["INVALID_FORMAT"]("Parámetros de paginación inválidos")

    # Traer todas las predicciones de partidos que ya tienen resultado cargado
    result = execute("""
        SELECT p.usuario_id, p.goles_local as pred_local, p.goles_visitante as pred_visitante,
               pa.goles_local as real_local, pa.goles_visitante as real_visitante
        FROM predicciones p
        JOIN partidos pa ON p.partido_id = pa.id
        WHERE pa.goles_local IS NOT NULL
    """)

    if result == False:
        return ERRORS["UNKNOWN_ERROR"]("Error al calcular el ranking")

    if not result:
        return '', 204

    puntos_por_usuario = {}
    for pred in result:
        uid = pred['usuario_id']
        if uid not in puntos_por_usuario:
            puntos_por_usuario[uid] = 0
        puntos_por_usuario[uid] += calcular_puntos(pred)

    ranking_completo = construir_ranking(puntos_por_usuario)

    total = len(ranking_completo)
    pagina = ranking_completo[offset: offset + limit]
    links = build_links(total, offset, limit)

    return jsonify({"ranking": pagina, "_links": links}), 200
