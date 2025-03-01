# 🛒 Lista de Compras Bot

Este es un bot de Telegram diseñado para gestionar listas de compras. Permite a los usuarios crear listas, agregar productos y especificar cantidades de manera interactiva y fácil de usar.
## ⚠️ Este proyecto está en desarrollo y puede estar sujeto a cambios. ⚠️

## 🚀 Características

- Crear nuevas listas de compras.
- Agregar productos a listas existentes.
- Especificar la cantidad de cada producto.
- Repetir el proceso de agregar productos sin necesidad de seleccionar nuevamente la lista.
- Opción de cancelar en cualquier momento enviando `0️⃣`.
- Mensajes con emojis para una mejor experiencia de usuario.

## 🛠 Instalación

### 1️⃣ Clonar el repositorio

```sh
    git clone https://github.com/BecerraIgnacio/ListaDeComprasBot.git
    cd ListaDeComprasBot
```

### 2️⃣ Crear un entorno virtual (opcional pero recomendado)

```sh
    python -m venv venv
    source venv/bin/activate  # En Linux/Mac
    venv\Scripts\activate     # En Windows
```

### 3️⃣ Instalar dependencias

```sh
    pip install -r requirements.txt
```

## 🚀 Uso

### 1️⃣ Configurar el token del bot

Edita el archivo `config.py` y reemplaza `TOKEN` con el token de tu bot de Telegram.

### 2️⃣ Ejecutar el bot

```sh
    python main.py
```

El bot comenzará a ejecutarse y podrás interactuar con él en Telegram.

## 📌 Comandos disponibles

- `/add` → Inicia la secuencia de agregar productos a una lista.

## 📜 Flujo de trabajo

1. El usuario ejecuta `/add`.
2. Se le pide el nombre de la lista.
3. Si la lista no existe, se pregunta si desea crearla.
4. Se solicita el nombre del producto.
5. Se solicita la cantidad del producto.
6. Se repite el proceso hasta que el usuario envíe `0️⃣` para salir.

## 🛠 Tecnologías utilizadas

- Python 3
- `python-telegram-bot`

---

En desarrollo por Ignacio Becerra

