from flask import Blueprint
from controllers.ranking_controllers import *

ranking_bp = Blueprint('ranking', __name__)

ranking_bp.route('/', methods=['GET'])(obtener_ranking)