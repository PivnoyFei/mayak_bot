import telebot

from db import Parsing, engine
from settings import TOKEN
from utils import file_check, file_send, parser, waiting_for_file

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
    """
    Получает файл от пользователя и делает его проверку "file_check".
    Если файл соотвествует, пробует сохранить.
    Если такой магазин уже есть ловит исключение и предупреждает пользователя.
    """
    items = file_check(bot, message)
    if not items:
        return waiting_for_file(bot, message)
    send_message = []
    for name, url, xpath in zip(*items):
        if not db_parsing.create(name, url, xpath):
            bot.send_message(
                message.chat.id, f"Имя - {name}, уже есть в базе данных"
            )
        average = parser(url, xpath)
        send_message.append((
            f"name - {name}",
            f"url - {url}",
            f"xpath - {xpath}",
            f"Средняя стоймость зюзюблика - {average}"
        ))
    file_send(bot, message, send_message)


if __name__ == '__main__':
    if TOKEN:
        bot.infinity_polling()
    else:
        print("Нет переменной TOKEN")
