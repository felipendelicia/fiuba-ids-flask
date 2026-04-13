from flask import Blueprint
from controllers.partidos_controllers import *

partidos_bp = Blueprint('partidos', __name__)

# Endpoints Obligatorios 
partidos_bp.route('/', methods=['GET'])(listar_partidos)
partidos_bp.route('/', methods=['POST'])(crear_partido)
partidos_bp.route('/<int:id>', methods=['GET'])(obtener_partido) 
partidos_bp.route('/<int:id>', methods=['DELETE'])(eliminar_partido) 
partidos_bp.route('/<int:id>/resultado', methods=['PUT'])(cargar_resultado) 

# Predicciones (Enunciado Sorpresa)
partidos_bp.route('/<int:id>/prediccion', methods=['POST'])(registrar_prediccion) 

# Endpoints Opcionales 
partidos_bp.route('/<int:id>', methods=['PUT'])(reemplazar_partido) 
partidos_bp.route('/<int:id>', methods=['PATCH'])(actualizar_partido_parcial) 