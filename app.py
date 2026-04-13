import os

from dotenv import load_dotenv
from flask import Flask

from routes.partidos_routes import partidos_bp
from routes.usuarios_routes import usuarios_bp
from routes.ranking_routes import ranking_bp

load_dotenv()

app = Flask(__name__)

app.register_blueprint(partidos_bp, url_prefix='/partidos')
app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
app.register_blueprint(ranking_bp, url_prefix='/ranking')

if __name__ == '__main__':
    if os.getenv('ENV') == 'dev':
        app.run(debug=True, port=os.getenv('FLASK_PORT'))
    else:
        app.run(debug=False,host='0.0.0.0', port=os.getenv('FLASK_PORT'))
    
    