# PrecioRastreo

Este proyecto permite rastrear y registrar los precios de productos de manera automática, almacenando los resultados y notificando cambios relevantes.

## Estructura del proyecto
- `main.py`: Script principal para ejecutar el rastreador.
- `tracker.py`: Lógica de rastreo de precios.
- `products_manager.py`: Gestión de productos a rastrear.
- `notifier.py`: Notificaciones de cambios de precio.
- `config_manager.py`: Manejo de configuración.
- `database.py`: Gestión de almacenamiento de datos.
- `config.json`: Archivo de configuración general (incluye token y chat_id para notificaciones por Telegram).
- `productos.json`: Lista de productos a rastrear y su historial de precios.
- `requirements.txt`: Dependencias del proyecto.
- `main.spec`: Configuración para generar el ejecutable con PyInstaller.
- `dist/main.exe`: Ejecutable generado para Windows.

## Requisitos
- Python 3.10 o superior
- Instalar las dependencias:

```powershell
pip install -r requirements.txt
```

## Uso

### Ejecución manual (Python)

```powershell
python main.py
```

### Ejecución como ejecutable (Windows)

```powershell
dist\main.exe
```

### Ejecución diaria automática

Puedes programar la ejecución diaria usando el programador de tareas de Windows. Por ejemplo, crea una tarea que ejecute:

```powershell
python daily_check.py
```

o bien el ejecutable:

```powershell
dist\main.exe
```

## Notificaciones
El sistema puede enviar notificaciones por Telegram cuando detecta cambios de precio, según la configuración en `config.json`.

## Contacto
Para dudas o sugerencias, contacta al autor del repositorio.
