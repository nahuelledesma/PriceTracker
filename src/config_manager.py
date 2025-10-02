import json
import os

CONFIG_FILE = "config.json"

def load_config():
    """Carga la configuración del bot desde config.json."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return None
    return None

def save_config(config):
    """Guarda la configuración del bot en config.json."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

def setup_bot():
    """Configuración del bot por consola (opcional, para mantener compatibilidad)."""
    token = input("Ingrese el TOKEN del bot: ").strip()
    chat_id = input("Ingrese el CHAT_ID: ").strip()
    save_config({"token": token, "chat_id": chat_id})

def show_instructions():
    """Muestra instrucciones por consola (opcional)."""
    instrucciones = (
        "=== Instrucciones para crear el bot de Telegram ===\n\n"
        "1. Abrí Telegram y buscá 'BotFather'.\n"
        "2. Enviá el comando /newbot y seguí los pasos.\n"
        "3. Guardá el TOKEN que te da BotFather.\n"
        "4. Abrí un chat con tu bot y enviá cualquier mensaje.\n"
        "5. Para obtener tu chat_id, visitá:\n"
        "   https://api.telegram.org/bot<TU_TOKEN>/getUpdates\n"
        "6. Reemplazá <TU_TOKEN> por tu TOKEN y buscá 'chat': {\"id\": ...}\n"
        "7. Ese número es tu chat_id.\n"
    )
    print(instrucciones)
