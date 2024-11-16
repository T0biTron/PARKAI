# ai/train_model.py
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import joblib
import matplotlib.pyplot as plt

# Ruta del archivo CSV (relativa, porque está en la misma carpeta que este script)
csv_path = "parking_data.csv"

# Verificar si el archivo CSV existe
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"El archivo CSV no se encontró en la ruta: {csv_path}")

# Cargar los datos históricos de ocupación del parqueadero
data = pd.read_csv(csv_path)

# Renombrar columnas si los nombres son diferentes
data.rename(columns={
    'Hora': 'hora',
    'Dia': 'dia',
    'Tipo_espacio': 'tipo_espacio',
    'Temporada': 'temporada',
    'Ocupacion': 'ocupacion'
}, inplace=True)

# Limpiar espacios en blanco en la columna 'hora'
data['hora'] = data['hora'].str.strip()

# Convertir "Hora" a formato numérico (de texto como "10:00am" a 24 horas)
if data['hora'].dtype == 'object':
    data['hora'] = pd.to_datetime(data['hora'], format='%I:%M%p', errors='coerce').dt.hour

# Imprimir la columna 'hora' para verificar
print(data['hora'])

# Verificar cuántos valores no se han convertido
print("Valores no convertidos:", data['hora'].isna().sum())

# Codificar datos categóricos a valores numéricos
label_encoder = LabelEncoder()
data['dia'] = label_encoder.fit_transform(data['dia'])  # Ejemplo: lunes -> 0, martes -> 1, ...
data['tipo_espacio'] = label_encoder.fit_transform(data['tipo_espacio'])  # Ejemplo: normal -> 0, ...
data['ocupacion'] = label_encoder.fit_transform(data['ocupacion'])  # Ejemplo: libre -> 0, ocupado -> 1

# Preprocesamiento de datos
X = data[['hora', 'dia', 'tipo_espacio', 'temporada']].values
y = data['ocupacion'].values

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Escalado de datos
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Guardar el scaler para usarlo en producción
scaler_path = "scaler.pkl"
joblib.dump(scaler, scaler_path)
print(f"Scaler guardado en {scaler_path}")

# Definir la red neuronal
model = Sequential()
model.add(Dense(16, input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))  # Salida binaria para ocupación (1 o 0)

# Compilar el modelo
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Entrenar el modelo
history = model.fit(X_train, y_train, epochs=50, batch_size=10, validation_data=(X_test, y_test))

# Guardar el modelo entrenado
model_path = "parking_model.h5"
model.save(model_path)
print(f"Modelo de ocupación guardado como '{model_path}'")

# Visualización del desempeño del modelo
plt.figure(figsize=(12, 5))

# Gráfico de pérdida
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Pérdida de entrenamiento')
plt.plot(history.history['val_loss'], label='Pérdida de validación')
plt.title('Pérdida durante el entrenamiento')
plt.xlabel('Época')
plt.ylabel('Pérdida')
plt.legend()

# Gráfico de precisión
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Precisión de entrenamiento')
plt.plot(history.history['val_accuracy'], label='Precisión de validación')
plt.title('Precisión durante el entrenamiento')
plt.xlabel('Época')
plt.ylabel('Precisión')
plt.legend()

plt.tight_layout()
plt.show()
