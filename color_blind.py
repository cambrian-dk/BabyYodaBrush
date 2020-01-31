from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)

import daltonize
import configparser
from PIL import Image
import os


PHOTO, MODE, KIND = range(3)
LUCKY_PHOTO = range(1)

config = configparser.ConfigParser()
config.read("config.ini")
telegram_key = config['Keys']['telegram']

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def lucky(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id, "Please send me an image.")

    return LUCKY_PHOTO

def lucky_photo(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id, "Processing.....please wait.")
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('images/test/local.jpg')
    image = Image.open('images/test/local.jpg')
    width = image.size[0]
    height = image.size[1]
    print('photo received')
    os.system('python3 filterAI2.py --mode gen')
    print('done calling')
    # ------------ ADD YOUR AI IMAGE PROCESSING HERE --------------------
    new_image = Image.open('output.jpg')
    print('image opened')
    # new_image = cv2.resize(new_image, (255, 255 * height / width))
    # print('image resized')
    # new_image.save('output.jpg')
    # print('image saved')
    context.bot.send_photo(chat_id, photo=open('output.jpg', 'rb'))
    context.bot.send_message(chat_id, "Here you go.")
    return -1;

def accessibility(update, context):

    chat_id = update.effective_chat.id

    context.bot.send_message(chat_id, "Please send me an image...")
    return PHOTO

def photo(update, context):
    user = update.message.from_user

    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')

    reply_keyboard = [['Daltonize', 'Simulate']]
    update.message.reply_text("Alright, which mode would you prefer?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return MODE;

def mode(update, context):
    user = update.message.from_user
    # m = update.message.text
    context.user_data['mode'] = update.message.text
    reply_keyboard = [['Deuteranopia', 'Protanopia', 'Tritanopia']]
    update.message.reply_text('Alright, please choose a type of color blindness.', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    return KIND


def kind(update, context):
    user = update.message.from_user
    context.user_data['kind'] = update.message.text
    if context.user_data['mode'] == 'Daltonize':
        # print("Daltonizeeeeee")
        pic_simul_rgb = daltonize.daltonize(Image.open('user_photo.jpg'), str(context.user_data['kind']).lower()[0])
        simul_img = daltonize.array_to_img(pic_simul_rgb)
        simul_img.save('user_photo.jpg')
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('user_photo.jpg', 'rb'))
    else :
        # print("Simulateeeeee")
        pic_simul_rgb = daltonize.simulate(Image.open('user_photo.jpg'), str(context.user_data['kind']).lower()[0])
        simul_img = daltonize.array_to_img(pic_simul_rgb)
        simul_img.save('user_photo.jpg')
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('user_photo.jpg', 'rb'))

    print(context.user_data)
    update.message.reply_text('Here you go.')
    return -1

def cancel(update, context):
    user = update.message.from_user
    update.message.reply_text('Byeeeeee!')
    return -1 

def main():
    updater = Updater(token=telegram_key, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('accessibility', accessibility)],

        states = {
            PHOTO: [MessageHandler(Filters.photo, photo)],
            MODE: [MessageHandler(Filters.text, mode)],
            KIND: [MessageHandler(Filters.text, kind)]
        },

        fallbacks = [CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)
    
    lucky_handler = ConversationHandler(
        entry_points = [CommandHandler('lucky', lucky)],
        states = {
            LUCKY_PHOTO: [MessageHandler(Filters.photo, lucky_photo)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )
    dp.add_handler(lucky_handler)
    dp.add_handler(CommandHandler('cancel', cancel))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()