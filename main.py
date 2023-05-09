from googletrans import Translator
import telebot
import utils
from models.models import *
from db_session import env, session
import alembic.config
import uvicorn
import os
import soundfile as sf
import speech_recognition as sr
from datetime import datetime, timedelta
from schemas import Cashe_add, Cashe_all
from fastapi import FastAPI
from typing import Any

recognizer = sr.Recognizer()
bot = telebot.TeleBot(env("TOKEN"))
app = FastAPI()

@app.get("/cache/get_all")
def get_all_cache() -> list[Cashe_all]:
    q = session.query(Cache).all()
    list_of_cache = []
    for c in q:
        list_of_cache.append(Cashe_all(id=c.id_cache, date=c.date_of_activity, text_of_message=c.text_of_message, language_code=c.language_code, translated_text=c.russian_translation))
    return list_of_cache

@app.delete("/cache/delete")
def delete_cache() -> str:
    yesterday = datetime.now() - timedelta(days=1)
    deletion_cache = session.query(Cache).filter(Cache.date_of_activity < yesterday).delete(synchronize_session="fetch")
    session.commit()
    return "successful!"


@app.post("/cache/add")
def create_cache(item: Cashe_add) -> Cashe_add:
    cache = Cache()
    cache.text_of_message = item.text_of_message
    cache.language_code = item.language_code
    cache.date_of_activity = item.date
    cache.russian_translation = item.translated_text
    session.add(cache)
    session.commit()
    return item


# @app.post("/create_cache")
# def create_cache(text_of_message: str, language_code: str, translated_text: str):
#     cache = Cache()
#     cache.text_of_message = text_of_message
#     cache.language_code = language_code
#     cache.date_of_activity = datetime.datetime.now()
#     cache.russian_translation = translated_text
#     session.add(cache)
#     session.commit()
#     return "successfully added!"

@app.get("/cache/get_cache_by_text_message")
def get_cache(text_mess: str) -> Any:
    check_cache = session.query(Cache).filter(Cache.text_of_message == text_mess).first()
    try:
        return Cache(id_cache=check_cache.id_cache, date_of_activity=check_cache.date_of_activity, text_of_message=check_cache.text_of_message, \
                 language_code=check_cache.language_code, russian_translation=check_cache.russian_translation)
    except:
        return "no such cache."


@app.get("/translation/get")
def get_translation(text_mess: str) -> list[str]:
    translator = Translator()
    translated_text = translator.translate(text_mess, dest="ru")
    return translated_text.text, translated_text.src


@app.get("/translation_into_ru_by_cache_or_translator")
def translation_into_ru(text_mess: str) -> str:
    check_cache = get_cache(text_mess)
    if check_cache == "no such cache.":
        translated_text, translated_src = get_translation(text_mess)
        mess = f'{translated_text} \n\n(переведено с {utils.dict_of_lang[translated_src]})'
        #create_cache(text_mess, translated_src, translated_text)
        create_cache(Cashe_add(text_of_message=text_mess, language_code=translated_src, translated_text=translated_text,))
    else:
        mess = f'{check_cache.russian_translation} \n\n(переведено с {utils.dict_of_lang[check_cache.language_code]})'
    return mess


def recognise(filename: str) -> str:
    with sr.AudioFile(filename) as source:
        audio_text = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio_text, language='en-GB')
            return text
        except:
            return "Sorry.. run again..."


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     'Привет! Давай начнем! Отправляй мне любое сообщение, а я переведу его на русский язык!')


@bot.message_handler(func=lambda m: True)
def text_processing(message):
    bot.reply_to(message, translation_into_ru(message.text))


@bot.message_handler(content_types=['voice'])
def voice_processing(message):

    file_info = bot.get_file(message.voice.file_id)
    filename = str(file_info.file_id)
    file_name_full = "./voice/"+filename+".ogg"
    file_name_full_converted = "./ready/"+filename+".wav"

    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)

    data, samplerate = sf.read(file_name_full)
    sf.write(file_name_full_converted, data, samplerate)

    text = recognise(file_name_full_converted)
    if text == "Sorry.. run again...":
        bot.reply_to(message, text)
    else:
        bot.reply_to(message, translation_into_ru(text))
    os.remove(file_name_full)
    os.remove(file_name_full_converted)


if __name__ == "__main__":
    alembicArgs = [
        '--raiseerr',
        'upgrade', 'head',
    ]
    #alembic.config.main(argv=alembicArgs)
    uvicorn.run(app, host="127.0.0.1", port=8000)
    bot.infinity_polling()



