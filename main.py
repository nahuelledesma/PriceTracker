from tkinter import Tk, Label, Button, Entry, StringVar, Toplevel, Text, END, messagebox, simpledialog, Scrollbar, VERTICAL, RIGHT, Y
from datetime import datetime
from config_manager import load_config, save_config
from products_manager import load_products, save_products
from notifier import send_message
from tracker import check_price

# ----------------- Funciones -----------------

def show_instructions():
    instrucciones = (
        "=== Instrucciones para crear el bot de Telegram ===\n\n"
        "1. Abrí Telegram y buscá 'BotFather'.\n"
        "2. Enviá el comando /newbot y seguí los pasos.\n"
        "3. Guardá el TOKEN que te da BotFather.\n"
        "4. Abrí un chat con tu bot y enviá cualquier mensaje.\n"
        "5. Para obtener tu chat_id, visitá:\n"
        "   https://api.telegram.org/bot<TU_TOKEN>/getUpdates\n"
        "6. Reemplazá <TU_TOKEN> por tu TOKEN y buscá 'chat': {\"id\": ...}\n"
        "7. Ese número es tu chat_id.\n\n"
        "Luego podés configurar el bot en la opción correspondiente."
    )
    win = Toplevel()
    win.title("Instrucciones")
    text_area = Text(win, wrap="word", width=80, height=20)
    text_area.pack(expand=True, fill="both")
    text_area.insert(END, instrucciones)
    text_area.config(state="disabled")

def configurar_bot():
    config = load_config() or {}
    token_var = StringVar(value=config.get("token", ""))
    chat_id_var = StringVar(value=config.get("chat_id", ""))

    def guardar():
        token = token_var.get().strip()
        chat_id = chat_id_var.get().strip()
        if not token or not chat_id:
            messagebox.showerror("Error", "Debe ingresar TOKEN y CHAT_ID")
            return
        save_config({"token": token, "chat_id": chat_id})
        messagebox.showinfo("Éxito", "Bot configurado correctamente")
        win.destroy()

    win = Toplevel()
    win.title("Configurar Bot")
    Label(win, text="TOKEN:").pack()
    Entry(win, textvariable=token_var, width=50).pack()
    Label(win, text="CHAT_ID:").pack()
    Entry(win, textvariable=chat_id_var, width=50).pack()
    Button(win, text="Guardar", command=guardar).pack(pady=5)

def agregar_producto():
    nombre = simpledialog.askstring("Agregar producto", "Nombre del producto:")
    if not nombre:
        return
    url = simpledialog.askstring("Agregar producto", "URL del producto:")
    if not url:
        return
    sitio = simpledialog.askstring("Agregar producto", "Sitio del producto (ej: MercadoLibre):")
    if not sitio:
        return

    products = load_products()
    next_id = max([p["id"] for p in products], default=0) + 1
    new_product = {
        "id": next_id,
        "nombre": nombre.strip(),
        "url": url.strip(),
        "sitio": sitio.strip(),
        "historial": []
    }
    products.append(new_product)
    save_products(products)
    messagebox.showinfo("Producto agregado", f"✅ Producto agregado con ID {next_id}")

def eliminar_producto():
    products = load_products()
    if not products:
        messagebox.showwarning("Eliminar producto", "⚠️ No hay productos registrados.")
        return

    # Lista de nombres para mostrar
    nombres = [f"{p['id']}: {p['nombre']}" for p in products]
    seleccion = simpledialog.askstring(
        "Eliminar producto", 
        "Productos:\n" + "\n".join(nombres) + "\n\nIngrese el ID a eliminar:"
    )
    if not seleccion:
        return
    try:
        id_to_remove = int(seleccion)
        products = [p for p in products if p["id"] != id_to_remove]
        save_products(products)
        messagebox.showinfo("Eliminar producto", "✅ Producto eliminado.")
    except ValueError:
        messagebox.showerror("Error", "❌ ID inválido.")

def listar_productos():
    products = load_products()
    if not products:
        messagebox.showinfo("Productos", "⚠️ No hay productos registrados.")
        return

    win = Toplevel()
    win.title("Lista de productos")
    win.geometry("700x400")

    scrollbar = Scrollbar(win, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    text_area = Text(win, wrap="word", yscrollcommand=scrollbar.set)
    text_area.pack(expand=True, fill="both")
    scrollbar.config(command=text_area.yview)

    for p in products:
        historial_len = len(p["historial"])
        last_date = p["historial"][-1]["fecha"] if historial_len > 0 else "N/A"
        last_price = p["historial"][-1]["precio"] if historial_len > 0 else "N/A"
        text_area.insert(END, f"ID: {p['id']} - {p['nombre']} ({p['sitio']})\nURL: {p['url']}\nÚltimo precio: {last_price} | Fecha: {last_date}\nHistorial: {p['historial']}\n\n")
    text_area.config(state="disabled")

def probar_notificacion():
    config = load_config()
    if config:
        try:
            send_message(config["token"], config["chat_id"], "✅ Test de notificación OK!")
            messagebox.showinfo("Notificación", "✅ Test de notificación enviada.")
        except Exception as e:
            messagebox.showerror("Error", f"❌ No se pudo enviar la notificación:\n{e}")
    else:
        messagebox.showerror("Error", "❌ Debes configurar primero el bot.")

def revisar_precios():
    config = load_config()
    if not config:
        messagebox.showerror("Error", "❌ Debes configurar primero el bot.")
        return

    products = load_products()
    if not products:
        messagebox.showwarning("Revisar precios", "⚠️ No hay productos registrados.")
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

        try:
            send_message(config["token"], config["chat_id"], msg)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar la notificación para {product['nombre']}:\n{e}")

    save_products(products)
    messagebox.showinfo("Revisión completada", "✅ Notificaciones enviadas a todos los productos.")

# ----------------- Interfaz Tkinter -----------------

root = Tk()
root.title("Rastreador de Precios")
root.geometry("450x500")

Label(root, text="=== Rastreador de Precios ===", font=("Arial", 16)).pack(pady=10)

Button(root, text="1. Instrucciones para crear el bot", width=40, command=show_instructions).pack(pady=5)
Button(root, text="2. Configurar el bot (TOKEN y CHAT_ID)", width=40, command=configurar_bot).pack(pady=5)
Button(root, text="3. Agregar un producto para rastrear", width=40, command=agregar_producto).pack(pady=5)
Button(root, text="4. Eliminar un producto", width=40, command=eliminar_producto).pack(pady=5)
Button(root, text="5. Listar productos", width=40, command=listar_productos).pack(pady=5)
Button(root, text="6. Probar notificación", width=40, command=probar_notificacion).pack(pady=5)
Button(root, text="7. Revisar precios ahora", width=40, command=revisar_precios).pack(pady=5)
Button(root, text="0. Salir", width=40, command=root.quit).pack(pady=5)

root.mainloop()
