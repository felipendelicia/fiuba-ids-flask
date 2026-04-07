from flask import Blueprint
from controllers.usuarios_controllers import *

usuarios_bp = Blueprint('usuarios', __name__)


usuarios_bp.route('/', methods=['POST'])(crear_usuario)
usuarios_bp.route('/', methods=['GET'])(listar_usuarios)
usuarios_bp.route('/<int:id>', methods=['GET'])(obtener_usuario) 
usuarios_bp.route('/<int:id>', methods=['PUT'])(reemplazar_usuario)
usuarios_bp.route('/<int:id>', methods=['DELETE'])(eliminar_usuario)