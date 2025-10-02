import json
import os
from datetime import datetime

PRODUCTS_FILE = "productos.json"

def load_products():
    if not os.path.exists(PRODUCTS_FILE):
        return []
    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_products(products):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4)

def add_product():
    products = load_products()
    nombre = input("Nombre del producto: ")
    url = input("URL del producto: ")
    sitio = input("Sitio (ej: MercadoLibre): ")

    next_id = max([p["id"] for p in products], default=0) + 1
    new_product = {
        "id": next_id,
        "nombre": nombre.strip(),
        "url": url.strip(),
        "sitio": sitio.strip(),
        "historial": []  # historial vacío al inicio
    }
    products.append(new_product)
    save_products(products)
    print(f"✅ Producto agregado con ID {next_id}")


def remove_product():
    products = load_products()
    if not products:
        print("⚠️ No hay productos registrados.")
        return

    print("\nProductos rastreados:")
    for p in products:
        print(f"{p['id']}. {p['nombre']} -> {p['url']}")

    try:
        id_to_remove = int(input("Ingresa el ID del producto a eliminar: "))
        products = [p for p in products if p["id"] != id_to_remove]
        save_products(products)
        print("✅ Producto eliminado.")
    except ValueError:
        print("❌ ID inválido.")

def list_products():
    products = load_products()
    if not products:
        print("⚠️ No hay productos registrados.")
        return
    print("\n=== Lista de productos ===")
    for p in products:
        historial_len = len(p["historial"])
        last_date = p["historial"][-1]["fecha"] if historial_len > 0 else "N/A"
        last_price = p["historial"][-1]["precio"] if historial_len > 0 else "N/A"
        print(f"{p['id']} - {p['nombre']} ({p['url']}) | Último precio: {last_price} | Fecha: {last_date}")
