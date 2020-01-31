from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import urllib.request
import daltonize
import configparser
from PIL import Image
import os


config = configparser.ConfigParser()
config.read("config.ini")
telegram_key = config['Keys']['telegram']


updater = Updater(token=telegram_key, use_context=True)
dispatcher = updater.dispatcher
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    photo_link = os.path.join(os.path.dirname(__file__), 'test.png')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(photo_link, 'rb'))

def return_image(update, context):
    pic = context.bot.getFile(update.message.photo[-1].file_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="I RECIEVED AN IMAGE")
    urllib.request.urlretrieve(pic.file_path, 'local.jpg')
    photo_link = os.path.join(os.path.dirname(__file__), 'local.jpg')
    pic_simul_rgb = daltonize.daltonize(Image.open(photo_link), "p")
    simul_img = daltonize.array_to_img(pic_simul_rgb)
    simul_img.save('local.jpg')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(photo_link, 'rb'))

echo_handler = MessageHandler(Filters.text, echo)
image_handler = MessageHandler(Filters.photo, return_image)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(image_handler)
updater.start_polling()