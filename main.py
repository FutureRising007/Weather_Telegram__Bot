from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from weather import get_forecasts
from flask import Flask, request
import telebot
import os

# check for new messages --> polling
updater = Updater(token="2127480280:AAHA_sDSFoZuPDoroXveI9CQUizuqCYWRPY")
server = Flask(__name__)


# allows to register handler -> command, text, video, audio etc
dispatcher = updater.dispatcher


# define a command callback function
def start(update, context):
    context.bot.sendMessage(chat_id=update.message.chat_id, text="Hello, Welcome to Orion Alpha Weather Bot....")


# create a command handler
updater.dispatcher.add_handler(CommandHandler('start', start))

'''
def echo(update, context):
    update.sendMessage(chat_id=update.message.chat_id, text=update.message.text.upper())
# create a text handler
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)
'''

def option(update, context):
    button = [
        [InlineKeyboardButton("Option 1", callback_data="1"),
         InlineKeyboardButton("Option 2", callback_data="2")],
        [InlineKeyboardButton("Option 3", callback_data="3")]
    ]
    reply_markup = InlineKeyboardMarkup(button)

    context.bot.sendMessage(chat_id=update.message.chat_id,
                     text="Choose one option..",
                     reply_markup=reply_markup)


#option_handler = CommandHandler("option", option)
#dispatcher.add_handler(option_handler)

updater.dispatcher.add_handler(CommandHandler('option', option))

def get_location(update, context):
    button = [
        [KeyboardButton("Share Location", request_location=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(button)
    context.bot.sendMessage(chat_id=update.message.chat_id,
                     text="Mind sharing location?",
                     reply_markup=reply_markup)


#get_location_handler = CommandHandler("location", get_location)
#dispatcher.add_handler(get_location_handler)

updater.dispatcher.add_handler(CommandHandler('location', get_location))

def location(update, context):
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    forecasts = get_forecasts(lat, lon)
    context.bot.send_message(chat_id=update.message.chat_id,
                     text=forecasts,
                     reply_markup=ReplyKeyboardRemove())



#location_handler = MessageHandler(Filters.location, location)
#dispatcher.add_handler(location_handler)

updater.dispatcher.add_handler(MessageHandler(Filters.location, location))
# start polling
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://intense-oasis-82355.herokuapp.com/' + '6c84507cbe013046861cd673e1a59a75')
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))