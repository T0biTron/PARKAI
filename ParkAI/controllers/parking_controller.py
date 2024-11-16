# controllers/parking_controller.py
from flask import request, jsonify
from ai.load_model import predict_occupation

# Función para predecir la ocupación de un espacio de parqueo
def predict_parking_occupation():
    data = request.get_json()
    hora = data['hora']
    dia = data['dia']
    tipo_espacio = data['tipo_espacio']
    temporada = data['temporada']

    # Llamada al modelo de predicción
    ocupacion_predicha = predict_occupation(hora, dia, tipo_espacio, temporada)

    return jsonify({
        "ocupacion_predicha": int(ocupacion_predicha)
    })
