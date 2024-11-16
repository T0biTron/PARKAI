from flask import Flask, request, jsonify
from ai.load_model import predict_occupation

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.json
        hora = data['hora']
        dia = data['dia']
        tipo_espacio = data['tipo_espacio']
        temporada = data['temporada']

        # Hacer la predicción
        resultado = predict_occupation(hora, dia, tipo_espacio, temporada)
        return jsonify({"resultado": resultado}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
