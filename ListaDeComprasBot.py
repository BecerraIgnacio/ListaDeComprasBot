from config import TOKEN
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


# Definición de la clase ListaDeCompras
class ListaDeCompras:
    def __init__(self):
        self.listas = {}  # Diccionario para almacenar listas de compras
        self.usuario_estado = {}  # Diccionario para almacenar estados de usuarios

    async def iniciar_agregar_producto(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
        """Inicia el proceso de agregar un producto solicitando la lista."""
        await update.message.reply_text(
            "🛒 Ingrese el nombre de la lista a la que desea agregar productos.\n\n"
            "➕ Para crear una nueva lista, envíe un nuevo nombre.\n\n"
            "0️⃣ Para salir, envíe '0'."
        )
        self.usuario_estado[user_id] = "esperando_lista_agregar"

    async def iniciar_eliminar_producto(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
        """Inicia el proceso de eliminar un producto solicitando la lista."""
        await update.message.reply_text(
            "🛒 Ingrese el nombre de la lista de compras que desea modificar.\n\n"
            "Escriba 'all' para eliminar todas las listas.\n"
            "0️⃣ Para salir, envíe '0'."
        )
        self.usuario_estado[user_id] = "esperando_lista_eliminar"

    async def procesar_lista_agregar(self, update: Update, user_id: int, text: str):
        """Procesa la lista en la que se quiere agregar productos."""
        if text in self.listas:  # Si la lista existe
            self.usuario_estado[user_id] = "esperando_producto"
            self.usuario_estado["lista_actual"] = text
            await self.solicitar_producto(update, user_id)
        else:
            self.usuario_estado[user_id] = "confirmar_creacion_lista"
            self.usuario_estado["nombre_lista"] = text
            await update.message.reply_text(f'❓ La lista "{text}" no existe. ¿Desea crearla? (Sí/No)')

    async def procesar_lista_eliminar(self, update: Update, user_id: int, text: str):
        """Procesa la lista que el usuario desea eliminar o modificar."""
        if text == "all":
            if self.listas:
                self.listas.clear()
                self.usuario_estado.pop(user_id, None)
                await update.message.reply_text("🗑️ Todas las listas de compras han sido eliminadas.")
                return
            else:
                await update.message.reply_text("⚠️ No hay listas para eliminar.")
            self.usuario_estado.pop(user_id, None)
            return

        if text in self.listas:
            self.usuario_estado[user_id] = "esperando_producto_eliminar"
            self.usuario_estado["lista_actual"] = text
            await self.solicitar_producto_eliminar(update, user_id)
        else:
            await update.message.reply_text(f'⚠️ La lista "{text}" no existe. Intente nuevamente.')

    async def crear_lista(self, update: Update, user_id: int, text: str):
        """Crea una nueva lista si el usuario confirma."""
        if text.lower() in ["si", "sí"]:
            lista_nombre = self.usuario_estado.get("nombre_lista")
            self.listas[lista_nombre] = {}
            self.usuario_estado[user_id] = "esperando_producto"
            self.usuario_estado["lista_actual"] = lista_nombre
            await update.message.reply_text(f"✅ Lista '{lista_nombre.capitalize()}' creada exitosamente.")
            await self.solicitar_producto(update, user_id)
        elif text.lower() == "no":
            await update.message.reply_text("📝 Ingrese nuevamente el nombre de la lista.")
            self.usuario_estado[user_id] = "esperando_lista_agregar"
        else:
            await update.message.reply_text("❌ Por favor, responda con 'Sí' o 'No'.")

    async def solicitar_producto(self, update: Update, user_id: int):
        """Solicita al usuario que ingrese un producto para agregar."""
        await update.message.reply_text("📦 Ingrese el producto que desea agregar.\n0️⃣ Para salir, envíe '0'.")
        self.usuario_estado[user_id] = "esperando_producto"

    async def solicitar_producto_eliminar(self, update: Update, user_id: int):
        """Solicita al usuario que ingrese un producto para eliminar."""
        lista_actual = self.usuario_estado.get("lista_actual")
        await update.message.reply_text(
            f"📦 Ingrese el producto que desea eliminar de la lista '{lista_actual}'.\n"
            "Escriba 'all' para eliminar la lista completa.\n"
            "0️⃣ Para salir, envíe '0'."
        )

    async def agregar_producto(self, update: Update, user_id: int, text: str):
        """Guarda el nombre del producto y solicita la cantidad."""
        lista_actual = self.usuario_estado.get("lista_actual")
        self.usuario_estado[user_id] = "esperando_cantidad"
        self.usuario_estado["producto_actual"] = text
        await update.message.reply_text(f"🔢 Ingrese la cantidad para '{text.capitalize()}'.")

    async def confirmar_cantidad(self, update: Update, user_id: int, text: str):
        """Guarda la cantidad ingresada y confirma la acción."""
        lista_actual = self.usuario_estado.get("lista_actual")
        producto_actual = self.usuario_estado.get("producto_actual")

        try:
            cantidad = int(text)
            if cantidad <= 0:
                await update.message.reply_text("⬆️ Ingrese un número mayor a 0.")
                return
            self.listas[lista_actual][producto_actual] = cantidad
            await update.message.reply_text(f"✅ Se añadieron {cantidad} unidades de '{producto_actual.capitalize()}' a la lista '{lista_actual.capitalize()}'.")
            await self.solicitar_producto(update, user_id)
        except ValueError:
            await update.message.reply_text("❌ Por favor, ingrese un número válido.")

    async def eliminar_producto(self, update: Update, user_id: int, text: str):
        """Elimina un producto o toda la lista."""
        lista_actual = self.usuario_estado.get("lista_actual")

        if text == "all":
            del self.listas[lista_actual]
            self.usuario_estado.pop(user_id, None)
            await update.message.reply_text(f"🗑️ La lista '{lista_actual}' ha sido eliminada por completo.")
            return
        elif text in self.listas[lista_actual]:
            del self.listas[lista_actual][text]
            await update.message.reply_text(f"✅ '{text.capitalize()}' ha sido eliminado de la lista '{lista_actual.capitalize()}'.")
        else:
            await update.message.reply_text(f"⚠️ '{text.capitalize()}' no se encuentra en la lista '{lista_actual.capitalize()}'.")
        await self.solicitar_producto_eliminar(update, user_id)


    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja todas las respuestas de texto del usuario."""
        user_id = update.message.from_user.id
        text = update.message.text.strip().lower()

        if text == "0":
            await update.message.reply_text("Operación cancelada.")
            self.usuario_estado.pop(user_id, None)
            return

        estado = self.usuario_estado.get(user_id)

        if estado == "esperando_lista_agregar":
            await self.procesar_lista_agregar(update, user_id, text)
        elif estado == "confirmar_creacion_lista":
            await self.crear_lista(update, user_id, text)
        elif estado == "esperando_producto":
            await self.agregar_producto(update, user_id, text)
        elif estado == "esperando_cantidad":
            await self.confirmar_cantidad(update, user_id, text)
        elif estado == "esperando_lista_eliminar":
            await self.procesar_lista_eliminar(update, user_id, text)
        elif estado == "esperando_producto_eliminar":
            await self.eliminar_producto(update, user_id, text)



# Instancia global de lista de compras
lista_compras = ListaDeCompras()


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja el comando /add e inicia el proceso de selección de lista."""
    user_id = update.message.from_user.id
    print(f"Usuario {user_id} inició /add")
    await lista_compras.iniciar_agregar_producto(update, context, user_id)

async def del_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja el comando /add e inicia el proceso de selección de lista."""
    user_id = update.message.from_user.id
    print(f"Usuario {user_id} inició /del")
    await lista_compras.iniciar_eliminar_producto(update, context, user_id)


if __name__ == '__main__':
    print('Starting lista de compras')
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('add', add_command))
    app.add_handler(CommandHandler('del', del_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lista_compras.message_handler))
    app.run_polling(poll_interval=3)