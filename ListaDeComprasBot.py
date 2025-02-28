from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '7808648733:AAFgKfU6atT3IwE0HTO2qSBsisk378htz6M'
BOT_USEARNAME: Final = '@LisDeCom_bot'

### Definicion ListaDeCompras

class ListaDeCompras:
    # Inicializa lista de compras como diccionario
    def __init__(self):
        self.productos = {}

    # Funcion para agregar productos
    def agregar_producto(self, articulo: str, cantidad: int = 1):
        articulo = articulo.lower()
        if articulo in self.productos:
            self.productos[articulo] += cantidad
        else:
            self.productos[articulo] = cantidad

    # Funcion

# Instancia global de lista de compras
lista_compras = ListaDeCompras()


### Definicion de comandos

"""
Comando /add

El comando /add tendra la siguiente sintaxis

'/add (articulo)?(cantidad)'

Si no hay '?' se tomara como que estamos ingresando solo 1 (un) articulo
Si hay '?' se tomara como que estamos ingresando (cantidad) de articulo
"""


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_completo = ' '.join(context.args)
    if mensaje_completo != "":
        if '?' in mensaje_completo:
            partes = mensaje_completo.split('?')
            articulo = partes[0]

            # Probar si despues de '?' hay un numero
            try:
                # Si la cantidad es positiva es un dato valido
                if int(partes[1]) > 0:
                    cantidad = int(partes[1])
                    lista_compras.agregar_producto(articulo, cantidad)
                    print(f'Producto agregado con exito: {articulo}, {cantidad}')
                    response: str = '✅ Producto agregado con exito'
                else:
                    print('Numero no valido. Deben ser valores positivos.')
                    response: str = '❌ Error en el ingreso. Cantidad debe ser positiva.'

            except ValueError:
                    print('Numero no valido. Deben ser valores positivos.')
                    response: str = '❌ Error en el ingreso. Cantidad debe ser un numero.'

        else:
            articulo = mensaje_completo
            cantidad = 1
            lista_compras.agregar_producto(articulo, cantidad)
            print(f'Producto agregado con exito: {articulo}, {cantidad}')
            response: str = '✅ Producto agregado con exito'
    else:
        response: str = '❗ El comando /add debe tener el siguiente formato:\n"/add articulo"\no\n"/add articulo?cantidad"\n(El signo de pregunta es para dividir articulo de cantidad, debe ser parte del mensaje)\nEl comando /add solo NO es valido'

    print('Saliendo de /add')
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting lista de compras')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('add', add_command))
    app.add_error_handler(error)
    app.run_polling(poll_interval = 3)