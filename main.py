import telebot

from db import Parsing, engine
from settings import TOKEN
from utils import file_check, waiting_for_file

db_parsing = Parsing(engine)
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать, {0.first_name}!\nЯ — <b>{1.first_name}</b>.\n"
        "Не обращай внимания на название я создан что бы парсить зюзюбликов."
        .format(message.from_user, bot.get_me()),
        parse_mode="html"
    )
    waiting_for_file(bot, message)


@bot.message_handler(content_types=['document'])
def get_file(message):
    items = file_check(bot, message)
    if not items:
        return waiting_for_file(bot, message)
    for name, url, x in zip(*items):
        if not db_parsing.create(name, url, x):
            bot.send_message(
                message.chat.id, f"Имя - {name}, уже есть в базе данных"
            )
        bot.send_message(
            message.chat.id,
            f"name - {name}\n"
            f"url - {url}\n"
            f"x - {x}",
            parse_mode="html"
        )


if __name__ == '__main__':
    if TOKEN:
        bot.infinity_polling()
    else:
        print("Нет переменной TOKEN")
