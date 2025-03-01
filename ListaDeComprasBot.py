from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '7808648733:AAFgKfU6atT3IwE0HTO2qSBsisk378htz6M'
BOT_USEARNAME: Final = '@LisDeCom_bot'


# Definicion ListaDeCompras
class ListaDeCompras:
    def __init__(self):
        # Diccionario para almacenar las listas de compras
        self.listas = {}
        # Diccionario para almacenar el estado de cada usuario en el bot
        self.usuario_estado = {}

    async def elegir_lista(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Solicita al usuario que ingrese el nombre de la lista de compras."""
        user_id = update.message.from_user.id
        print(f"Usuario {user_id} inició /add")
        await update.message.reply_text("Ingrese el nombre de la lista a la que desea agregar productos.\n\n"
                                        "Para crear una nueva lista, envíe un nuevo nombre.\n\n"
                                        "Para salir, envíe '0'.")
        # Guarda el estado del usuario para esperar el nombre de la lista
        self.usuario_estado[user_id] = "esperando_lista"

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
            if text in self.listas:  # Si la lista ya existe
                await update.message.reply_text(f"La lista '{text}' ya existe. Ingrese el producto que desea agregar.")
                self.usuario_estado[user_id] = "agregando_producto"
                self.usuario_estado["lista_actual"] = text
            else:
                # Si la lista no existe, se pide confirmación para crearla
                self.usuario_estado[user_id] = "confirmando_creacion"
                self.usuario_estado["nombre_lista"] = text
                await update.message.reply_text(f'La lista "{text}" no existe. ¿Desea crearla? (Sí/No)')

        elif self.usuario_estado.get(user_id) == "confirmando_creacion":
            if text.lower() in ["si", "sí"]:  # Si el usuario confirma la creación
                lista_nombre = self.usuario_estado.get("nombre_lista")
                self.listas[lista_nombre] = {}  # Se crea la lista como diccionario para productos y cantidades
                print(f"Lista creada: {lista_nombre}")
                await update.message.reply_text(
                    f"Lista '{lista_nombre}' creada exitosamente. Ingrese el producto que desea agregar.")
                self.usuario_estado[user_id] = "agregando_producto"
                self.usuario_estado["lista_actual"] = lista_nombre
            elif text.lower() == "no":  # Si el usuario rechaza la creación
                await update.message.reply_text("Ingrese nuevamente el nombre de la lista.")
                self.usuario_estado[user_id] = "esperando_lista"  # Se vuelve a pedir la lista
            else:
                await update.message.reply_text("Por favor, responda con 'Sí' o 'No'.")

        elif self.usuario_estado.get(user_id) == "agregando_producto":
            lista_actual = self.usuario_estado.get("lista_actual")
            if lista_actual:
                print(f"Producto recibido para lista '{lista_actual}': {text}")
                self.usuario_estado[user_id] = "esperando_cantidad"
                self.usuario_estado["producto_actual"] = text
                await update.message.reply_text(f"Ingrese la cantidad para '{text}'.")

        elif self.usuario_estado.get(user_id) == "esperando_cantidad":
            lista_actual = self.usuario_estado.get("lista_actual")
            producto_actual = self.usuario_estado.get("producto_actual")

            try:
                cantidad = int(text)
                if cantidad <= 0:
                    await update.message.reply_text("Ingrese un número mayor a 0.")
                    return

                if producto_actual in self.listas[lista_actual]:
                    self.listas[lista_actual][producto_actual] += cantidad
                else:
                    self.listas[lista_actual][producto_actual] = cantidad

                print(f"Producto agregado: {producto_actual} ({cantidad}) en la lista '{lista_actual}'")
                await update.message.reply_text(
                    f"Se añadieron {cantidad} unidades de '{producto_actual}' a la lista '{lista_actual}'.")
                self.usuario_estado.pop(user_id, None)  # Se elimina el estado del usuario
            except ValueError:
                await update.message.reply_text("Por favor, ingrese un número válido.")


# Instancia global de lista de compras
lista_compras = ListaDeCompras()


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja el comando /add e inicia el proceso de selección de lista."""
    await lista_compras.elegir_lista(update, context)




if __name__ == '__main__':
    """Función principal que inicializa el bot."""
    print('Starting lista de compras')
    app = Application.builder().token(TOKEN).build()

    # Agrega el manejador para el comando /add
    app.add_handler(CommandHandler('add', add_command))
    # Manejador para recibir las respuestas del usuario en la secuencia de listas y productos
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lista_compras.manejar_respuesta_lista))

    app.run_polling(poll_interval=3)  # Inicia el bot en modo polling
