from telegram import ReplyKeyboardMarkup, KeyboardButton, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler, CommandHandler, filters
import sys, subprocess, os

TOKEN = "xxxxxxxxxxxx"  //ingresa token de telegram
NAME, EMAIL = range(2)
mylist = []

def buttons():
    buttons = [[
        KeyboardButton ("DESBLOQUEAR")
    ],[
        KeyboardButton ("RESETEAR"),
        KeyboardButton ("BLOQUEAR CUENTA")
    ]]
    keyboardbutton = ReplyKeyboardMarkup(buttons)
    return keyboardbutton

def holaCallback(update, callback):
    update.message.reply_text ("Bienvenido a INCISO de la PLATAFORMA AUNA.")
    #update.message.reply_sticker(open("C:\\Users\\%user%\\Videos\\bottelegram\\bienvenido.tgs", 'rb'))
    update.message.reply_text ("¿Que operacion deseas realizar?. Te dejo las siguientes opciones", reply_markup=buttons())
    
    return NAME

def nameCallback(update, callback):
    operation = update.message.text
    mylist.append(f"{operation}")
    mylist[0] = f"{operation}"
    ll = mylist[0]
    keyboardMarkupRemove = ReplyKeyboardRemove()
    update.message.reply_text("INGRESA UN USUARIO", reply_markup=keyboardMarkupRemove)

    return EMAIL

def emailCallback(update, callback):
    update.message.reply_text("ESPERE...")
    user = update.message.text
    print (user)
    ll = mylist[0]
    operation = ll
    print (f"LA OPERACION QUE SE REALIZARA ES {operation}")
    if operation == "DESBLOQUEAR":
        try:
            p = subprocess.Popen(f"powershell.exe -c Get-ADUser -Identity {user} | Unlock-ADAccount", stdout=sys.stdout)
            p.communicate()
            update.message.reply_text("USUARIO DESBLOQUEADO. /empezar")
        except:
            update.message.reply_text("USUARIO NO EXISTE. /empezar")
    elif operation == "BLOQUEAR CUENTA":
        try:
            p = subprocess.Popen(f"powershell.exe -c Disable-ADAccount -Identity {user}", stdout=sys.stdout)
            p.communicate()
            update.message.reply_text("USUARIO INHABILITADO. /empezar")
        except:
            update.message.reply_text("USUARIO NO EXISTE. /empezar")
    elif operation == "RESETEAR":
        try:
            p = subprocess.Popen(f'powershell.exe -c Get-ADUser -Identity {user} | Unlock-ADAccount', stdout=sys.stdout)
            p.communicate()
            update.message.reply_text("USUARIO RESETEADO. /empezar")
        except:
            update.message.reply_text("USUARIO NO EXISTE. /empezar")
    else:
        update.message.reply_text("OPERACION INVALIDA, /empezar")


    return ConversationHandler.END


def fallbackCallback(update, callback):
    update.message.reply_text("DISCULPA, OPERACION INVALIDA, ESCOGE BIEN PE MONGOL")


def main() -> None:
    #CREAMOS UPDATER Y LE PASAMOS EL TOKEN
    updater = Updater(TOKEN)
    #OBTENEMOS EL DISPATCHER PARA REGISTRAR LOS HANDLERS
    dispatcher = updater.dispatcher
    #HANDLERS
    entry_points = [
        CommandHandler(f"empezar", holaCallback)
    ]
    states = {
        NAME: [
            MessageHandler(filters= Filters.text(["BLOQUEAR CUENTA", "RESETEAR", "DESBLOQUEAR"]) & ~Filters.update.edited_message & ~Filters.command, callback = nameCallback)
        ],
        EMAIL: [
            MessageHandler(filters = Filters.text & ~Filters.command & ~Filters.update.edited_message, callback = emailCallback)
        ]
    }
    fallbacks = [
        MessageHandler(filters = Filters.all, callback = fallbackCallback)
    ]
    dispatcher.add_handler(ConversationHandler(entry_points, states, fallbacks))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
