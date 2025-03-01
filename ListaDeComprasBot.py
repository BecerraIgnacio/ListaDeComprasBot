from config import TOKEN
from config import BOT_USEARNAME
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


# Definicion ListaDeCompras
class ListaDeCompras:
    def __init__(self):
        # Diccionario para almacenar las listas de compras
        self.listas = {}
        # Diccionario para almacenar el estado de cada usuario en el bot
        self.usuario_estado = {}

    async def elegir_lista(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
        """Solicita al usuario que ingrese el nombre de la lista de compras."""
        await update.message.reply_text("🛒 Ingrese el nombre de la lista a la que desea agregar productos.\n\n"
                                        "➕ Para crear una nueva lista, envíe un nuevo nombre.\n\n"
                                        "0️⃣ Para salir, envíe '0'.")
        # Guarda el estado del usuario para esperar el nombre de la lista
        self.usuario_estado[user_id] = "esperando_lista"

    async def confirmar_lista(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, text: str):
        """Confirma si la lista existe o necesita ser creada."""
        if text in self.listas:  # Si la lista ya existe
            self.usuario_estado[user_id] = "agregando_producto"
            self.usuario_estado["lista_actual"] = text
            await self.solicitar_producto(update, context, user_id)
        else:
            self.usuario_estado[user_id] = "confirmando_creacion"
            self.usuario_estado["nombre_lista"] = text
            await update.message.reply_text(f'❓ La lista "{text}" no existe. ¿Desea crearla? (Sí/No)')

    async def manejar_respuesta_lista(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja la respuesta del usuario cuando ingresa el nombre de la lista."""
        user_id = update.message.from_user.id
        text = update.message.text.strip()
        print(f"Usuario {user_id} envió: {text}")
        print(f"Estado actual del usuario: {self.usuario_estado.get(user_id)}")
        print(f"Listas de compras actuales: {self.listas}")

        if text == '0':  # Si el usuario ingresa '0', se cancela la operación
            await update.message.reply_text("Operación cancelada.")
            self.usuario_estado.pop(user_id, None)
            return

        if self.usuario_estado.get(user_id) == "esperando_lista":
            await self.confirmar_lista(update, context, user_id, text)
        elif self.usuario_estado.get(user_id) == "confirmando_creacion":
            await self.crear_lista(update, context, user_id, text)
        elif self.usuario_estado.get(user_id) == "agregando_producto":
            await self.solicitar_cantidad(update, context, user_id, text)
        elif self.usuario_estado.get(user_id) == "esperando_cantidad":
            await self.agregar_cantidad(update, context, user_id, text)

    async def crear_lista(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, text: str):
        """Crea una nueva lista si el usuario confirma."""
        if text.lower() in ["si", "sí"]:
            lista_nombre = self.usuario_estado.get("nombre_lista")
            self.listas[lista_nombre] = {}  # Se crea la lista como diccionario para productos y cantidades
            print(f"Lista creada: {lista_nombre}")
            self.usuario_estado[user_id] = "agregando_producto"
            self.usuario_estado["lista_actual"] = lista_nombre
            await update.message.reply_text(f"✅ Lista '{lista_nombre.capitalize()}' creada exitosamente.")
            await self.solicitar_producto(update, context, user_id)
        elif text.lower() == "no":
            await update.message.reply_text("📝 Ingrese nuevamente el nombre de la lista.")
            self.usuario_estado[user_id] = "esperando_lista"
        else:
            await update.message.reply_text("❌ Por favor, responda con 'Sí' o 'No'.")

    async def solicitar_producto(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
        """Solicita al usuario que ingrese el nombre del producto."""
        await update.message.reply_text("📦 Ingrese el producto que desea agregar.\n0️⃣ Para salir, envíe '0'.")
        self.usuario_estado[user_id] = "agregando_producto"

    async def solicitar_cantidad(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, text: str):
        """Solicita la cantidad del producto ingresado."""
        lista_actual = self.usuario_estado.get("lista_actual")
        if lista_actual:
            print(f"Producto recibido para lista '{lista_actual}': {text}")
            self.usuario_estado[user_id] = "esperando_cantidad"
            self.usuario_estado["producto_actual"] = text
            await update.message.reply_text(f"🔢 Ingrese la cantidad para '{text.capitalize()}'.")

    async def agregar_cantidad(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, text: str):
        """Agrega la cantidad ingresada al producto correspondiente y vuelve a solicitar otro producto."""
        lista_actual = self.usuario_estado.get("lista_actual")
        producto_actual = self.usuario_estado.get("producto_actual")
        try:
            cantidad = int(text)
            if cantidad <= 0:
                await update.message.reply_text("⬆️ Ingrese un número mayor a 0.")
                return
            if producto_actual in self.listas[lista_actual]:
                self.listas[lista_actual][producto_actual] += cantidad
            else:
                self.listas[lista_actual][producto_actual] = cantidad
            print(f"Producto agregado: {producto_actual} ({cantidad}) en la lista '{lista_actual}'")
            await update.message.reply_text(f"✅ Se añadieron {cantidad} unidades de '{producto_actual.capitalize()}' a la lista '{lista_actual.capitalize()}'.")
            await self.solicitar_producto(update, context, user_id)  # Volver a pedir otro producto
        except ValueError:
            await update.message.reply_text("❌ Por favor, ingrese un número válido.")


# Instancia global de lista de compras
lista_compras = ListaDeCompras()


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja el comando /add e inicia el proceso de selección de lista."""
    user_id = update.message.from_user.id
    print(f"Usuario {user_id} inició /add")
    await lista_compras.elegir_lista(update, context, user_id)


if __name__ == '__main__':
    print('Starting lista de compras')
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('add', add_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lista_compras.manejar_respuesta_lista))
    app.run_polling(poll_interval=3)