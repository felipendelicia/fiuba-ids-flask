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
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True) # dictionary=True para que devuelva dicts en vez de tuplas
        cursor.execute(query)
        conexion.commit()
        resultados = cursor.fetchall()

    except Exception as e:
        print(f"Error no controlado: {e}")         
        return False

    finally:
        cursor.close()
        conexion.close()

    return resultados

