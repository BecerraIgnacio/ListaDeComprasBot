# 🏢 Lista de Compras Bot

Este es un bot de Telegram diseñado para gestionar listas de compras. Permite a los usuarios crear listas, agregar y eliminar productos, y especificar cantidades de manera interactiva y fácil de usar.

## ⚠️ Este proyecto está en desarrollo y puede estar sujeto a cambios. ⚠️

## 🚀 Características

- Cada usuario tiene su propio almacenamiento de listas, **sin acceso a listas de otros usuarios**.
- Crear nuevas listas de compras.
- Agregar productos a listas existentes.
- Especificar la cantidad de cada producto.
- Eliminar productos individuales de una lista.
- Eliminar una lista completa de compras.
- Eliminar todas las listas de compras de un usuario con `all`.
- Repetir el proceso de agregar o eliminar productos sin necesidad de seleccionar nuevamente la lista.
- Opción de cancelar en cualquier momento enviando `0️⃣`.
- Mensajes con emojis para una mejor experiencia de usuario.
- Mostrar todas las listas con sus productos utilizando `/show`.
- Confirmación al crear nuevas listas.
- Comando `/help` para mostrar los comandos disponibles y su descripción.
- **Carga y descarga automática de listas de compras en un archivo JSON, asegurando la persistencia de datos**.

## 🛠 Instalación

### 1️⃣ Clonar el repositorio

```sh
git clone https://github.com/BecerraIgnacio/ListaDeComprasBot.git
cd ListaDeComprasBot
```

### 2️⃣ Instalar dependencias

```sh
pip install -r requirements.txt
```

## 🚀 Uso

### 1️⃣ Configurar el token del bot de forma segura

Crea un archivo `config.py` en la raíz del proyecto y define tu token de esta manera:

```python
TOKEN = 'tu_token_aqui'
BOT_USERNAME = '@nombre_de_tu_bot'
```

### 2️⃣ Ejecutar el bot

```sh
python main.py
```

El bot comenzará a ejecutarse y podrás interactuar con él en Telegram.

## 📌 Comandos disponibles

- `/add` → Inicia la secuencia de agregar productos a una lista.
- `/del` → Inicia la secuencia para eliminar productos o listas completas.
- `/show` → Muestra todas las listas de compras y sus productos.
- `/help` → Muestra la lista de comandos disponibles y su función.

## 📝 Flujo de trabajo

### 🔹 **Agregar productos**
1. El usuario ejecuta `/add`.
2. Se le pide el nombre de la lista.
3. Si la lista no existe, se pregunta si desea crearla.
4. Se solicita el nombre del producto.
5. Se solicita la cantidad del producto.
6. Se repite el proceso hasta que el usuario envíe `0️⃣` para salir.
7. **La lista de compras se guarda automáticamente en `listas.json` después de cada modificación.**

### 🔹 **Eliminar productos o listas**
1. El usuario ejecuta `/del`.
2. Se le pide el nombre de la lista a modificar.
3. Si la lista no existe, se muestra un mensaje de error.
4. Se solicita el nombre del producto a eliminar o se ofrece la opción de eliminar toda la lista enviando `all`.
5. Si el usuario elimina una lista completa, el proceso se cancela automáticamente.
6. Si el usuario elimina un producto, se le sigue preguntando hasta que envíe `0️⃣` para salir.
7. **La lista de compras se guarda automáticamente en `listas.json` después de cada modificación.**

### 🔹 **Mostrar listas y productos**
1. El usuario ejecuta `/show`.
2. Se muestra una lista con todas las listas de compras y sus productos.
3. Si no hay listas creadas, se informa al usuario.

## 💻 Carga y descarga de listas

- **Cada usuario tiene su propio almacenamiento de listas separado**.
- El bot carga automáticamente las listas de compras desde el archivo `listas.json` al iniciarse y guarda cualquier cambio en el mismo archivo después de cada modificación.
- Se usa el **ID del usuario como clave única** para identificar sus listas y evitar que otros usuarios puedan acceder a ellas.
- **Los datos son persistentes**, incluso después de reiniciar el bot.

## 🛠 Tecnologías utilizadas

- Python 3
- `python-telegram-bot`
- JSON para almacenamiento de datos

---

🤔🛠 ¡Nuevas funcionalidades próximamente!

💛💻 Desarrollado por Ignacio Becerra