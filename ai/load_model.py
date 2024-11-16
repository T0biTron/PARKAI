from tensorflow.keras.models import load_model
import joblib
import numpy as np

# Cargar el modelo y el escalador previamente guardados
model_path = "parking_model.h5"
scaler_path = "scaler.pkl"

try:
    model = load_model(model_path)
    scaler = joblib.load(scaler_path)
    print("Modelo y escalador cargados correctamente.")
except Exception as e:
    raise FileNotFoundError(f"Error al cargar el modelo o el escalador: {e}")

def predict_occupation(hora, dia, tipo_espacio, temporada):
    """
    Predice la ocupación de un espacio de estacionamiento basado en las características proporcionadas.

    Parámetros:
        hora (int): Hora del día en formato 24 horas (0-23).
        dia (int): Día de la semana (0: lunes, 1: martes, ..., 6: domingo).
        tipo_espacio (int): Tipo de espacio (0: normal, 1: discapacitado, 2: eléctrico).
        temporada (int): Temporada (0: baja, 1: alta).

    Retorna:
        str: "Ocupado" si el modelo predice ocupación, "Libre" de lo contrario.
    """
    try:
        # Preprocesar los datos de entrada
        input_data = np.array([[hora, dia, tipo_espacio, temporada]])
        input_data = scaler.transform(input_data)

        # Hacer la predicción
        prediction = model.predict(input_data)
        ocupacion_predicha = (prediction[0][0] > 0.5).astype(int)  # 1 para ocupado, 0 para libre

        return "Ocupado" if ocupacion_predicha == 1 else "Libre"
    except Exception as e:
        print(f"Error durante la predicción: {e}")
        return None

# Bloque de pruebas
if __name__ == "__main__":
    # Prueba con diferentes escenarios
    print("Prueba 1:")
    print(predict_occupation(hora=10, dia=0, tipo_espacio=0, temporada=0))  # Lunes, 10:00am, normal, temporada baja

    print("Prueba 2:")
    print(predict_occupation(hora=18, dia=4, tipo_espacio=1, temporada=1))  # Viernes, 6:00pm, discapacitado, temporada alta

    print("Prueba 3:")
    print(predict_occupation(hora=15, dia=3, tipo_espacio=2, temporada=0))  # Jueves, 3:00pm, eléctrico, temporada baja
