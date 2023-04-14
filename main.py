from googletrans import Translator
import telebot
from environs import Env
import utils

env = Env()
env.read_env()

bot = telebot.TeleBot(env("TOKEN"))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     'Привет! Давай начнем! Отправляй мне любое сообщение, а я переведу его на русский язык!')


@bot.message_handler(func=lambda m: True)
def translation_into_Ru(message):
    translator = Translator()
    translated_text = translator.translate(message.text, dest="ru")
    mess = f'{translated_text.text} \n\n(переведено с {utils.dict_of_lang[translated_text.src]})'
    bot.reply_to(message, mess)

if __name__=="__main__":
    bot.infinity_polling()