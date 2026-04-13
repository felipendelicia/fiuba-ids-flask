from flask import jsonify

ERRORS = {
    "MISSING_REQUIRED_FIELDS": lambda message: (
        jsonify(
            {
                "errors": [
                    {
                        "code": 400,
                        "message": message,
                        "level": "error",
                        "description": "No mandaste todos los campos obligatorios, capo.",
                    }
                ]
            }
        ),
        400,
    ),
    "CONFLICT": lambda message: (
        jsonify(
            {
                "errors": [
                    {
                        "code": 409,
                        "message": message,
                        "level": "error",
                        "description": "Hay conflictos con los registros existentes, capo.",
                    }
                ]
            }
        ),
        409,
    ),
    "INVALID_FORMAT": lambda message: (
        jsonify(
            {
                "errors": [
                    {
                        "code": 400,
                        "message": message,
                        "level": "error",
                        "description": "Formato enviado con los datos erroneo, capo",
                    }
                ]
            }
        ),
        400,
    ),
    "UNKNOWN_ERROR": lambda message: (
        jsonify(
            {
                "errors": [
                    {
                        "code": 500,
                        "message": message,
                        "level": "error",
                        "description": "Error desconocido, capo",
                    }
                ]
            }
        ),
        500,
    ),
    "NOT_FOUND": lambda message: (
        jsonify(
            {
                "errors": [
                    {
                        "code": 404,
                        "message": message,
                        "level": "error",
                        "description": "Registro no encontrado, capo",
                    }
                ]
            }
        ),
        404,
    ),
}
