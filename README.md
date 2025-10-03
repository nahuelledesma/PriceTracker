# PrecioRastreo

Este proyecto permite rastrear y registrar los precios de productos de manera automática, almacenando los resultados y notificando cambios relevantes.

## Estructura del proyecto (Árbol)

```
PrecioRastreo/
├── build/
│   └── main/
├── dist/
│   ├── config.json
│   ├── main.exe
│   └── productos.json
├── requirements.txt
├── src/
│   ├── config_manager.py
│   ├── daily_check.py
│   ├── database.py
│   ├── main.py
│   ├── main.spec
│   ├── notifier.py
│   ├── products_manager.py
│   └── tracker.py
├── README.md
```

## Requisitos
- Python 3.10 o superior
- Instalar las dependencias:

```powershell
pip install -r requirements.txt
```

## Uso

### Ejecución manual (Python)

```powershell
python src\main.py
```

### Ejecución como ejecutable (Windows)

```powershell
dist\main.exe
```

### Ejecución diaria automática

Puedes programar la ejecución diaria usando el programador de tareas de Windows. Por ejemplo, crea una tarea que ejecute:

```powershell
python src\daily_check.py
```

o bien el ejecutable:

```powershell
dist\main.exe
```

## Notificaciones
El sistema puede enviar notificaciones por Telegram cuando detecta cambios de precio, según la configuración en `config.json`.

## Contacto
Para dudas o sugerencias, contacta al autor del repositorio.
