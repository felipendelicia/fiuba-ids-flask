import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'host': 'localhost',
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE'),
    'port': os.getenv('MYSQL_PORT')
}

def get_db_connection():
    # Establece la conexión manual
    conn = mysql.connector.connect(**db_config)
    return conn

def execute(query):
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True) # dictionary=True para que devuelva dicts en vez de tuplas

    try:
        cursor.execute(query)
        resultados = cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()

    return resultados

