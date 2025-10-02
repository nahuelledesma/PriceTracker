from config_manager import load_config
from products_manager import load_products, save_products
from tracker import check_price
from notifier import send_message
from datetime import datetime

def main():
    config = load_config()
    if not config:
        print("❌ Debes configurar el bot primero.")
        return

    products = load_products()
    if not products:
        print("⚠️ No hay productos registrados.")
        return

    for product in products:
        price = check_price(product)
        if price is None:
            msg = f"{product['nombre']} ({product['sitio']})\n❌ No se pudo obtener el precio.\n{product['url']}"
        else:
            historial = product.get("historial", [])
            if historial:
                last_price = historial[-1]["precio"]
                if price > last_price:
                    estado = "El precio subió 📈"
                elif price < last_price:
                    estado = "El precio bajó 📉"
                else:
                    estado = "El precio se mantiene 📊"
            else:
                estado = "Primer registro ✅"

            historial.append({"fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "precio": price})
            product["historial"] = historial

            msg = (
                f"{product['nombre']} ({product['sitio']})\n"
                f"Precio actual: ${price:,.2f}\n"
                f"{estado}\n"
                f"{product['url']}"
            )

        send_message(config["token"], config["chat_id"], msg)

    save_products(products)
    print("✅ Revisión de precios completada.")

if __name__ == "__main__":
    main()
