# INTRODUCCIÓN AL DESARROLLO DE SOFTWARE
# BACKEND - FIUBA
# Fixture Mundialista 2026

## Integrantes
- Ronny Mamani Torrez 114779
- Felipe Nahuel Delicia Padron
- Nombre Apellidos Padron
- Nombre Apellidos Padron
- Nombre Apellidos Padron
- Nombre Apellidos Padron 

## Descripción
Este proyecto simula el funcionamiento de un fixture mundialista para el año 2026. El sistema permite a los usuarios consultar los partidos programados, los equipos participantes y los resultados de los encuentros. Además, se pueden realizar predicciones sobre los resultados de los partidos y comparar las predicciones con los resultados reales.

## Funcionalidades
- Consulta de partidos programados
- Agregar partidos programados
- Consulta de resultados de partidos
- Realización de predicciones sobre los resultados de los partidos

## Instalación

En el directorio del proyecto:

### Configurar variables de entorno

- cp .env.example .env
- Editar el archivo .env con las credenciales de la base de datos 

### Crear un entorno virtual e instalar las dependencias

- python3 -m venv .venv
- . .venv/bin/activate
- pip install -r requeriments.txt

### Crear esquema de base de datos

- sudo mysql < schema.sql

### Ejecutar el servidor

- flask run 