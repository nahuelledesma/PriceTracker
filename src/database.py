import pandas as pd
from datetime import datetime
import os

ARCHIVO = "data/precios.csv"

def guardar_precio(nombre, precio):
    """
    Guarda el precio en un archivo CSV con fecha
    """
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if os.path.exists(ARCHIVO):
        df = pd.read_csv(ARCHIVO)
    else:
        df = pd.DataFrame(columns=["fecha", "producto", "precio"])

    df = pd.concat([df, pd.DataFrame([[fecha, nombre, precio]], columns=df.columns)])
    df.to_csv(ARCHIVO, index=False)

def comparar_precio(precio_actual):
    """
    Compara el precio actual con el anterior y devuelve un mensaje
    """
    if os.path.exists(ARCHIVO):
        df = pd.read_csv(ARCHIVO)
        if len(df) > 1:
            precio_anterior = df.iloc[-2]["precio"]
            if precio_actual > precio_anterior:
                return "El precio subió 📈"
            elif precio_actual < precio_anterior:
                return "El precio bajó 📉"
            else:
                return "El precio se mantiene 📊"
    return "Primer registro ✅"
