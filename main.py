from aiogram import Bot, Dispatcher, executor, types

from db import Parsing, engine
from settings import TOKEN
from utils import file_check, file_send, parser, waiting_for_file

db_parsing = Parsing(engine)
bot = Bot(TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    print('Бот вышел в онлайн')


@dp.message_handler(commands=["start"])
async def start_message(message: types.Message):
    await bot.send_message(
        message.chat.id,
        "Добро пожаловать, {0.first_name}!\nЯ — <b>{1.first_name}</b>.\n"
        "Не обращай внимания на название я создан что бы парсить зюзюбликов."
        .format(message.from_user, await bot.get_me()),
        parse_mode="html"
    )
    await waiting_for_file(bot, message)


@dp.message_handler(content_types=['document'])
async def get_file(message: types.Message):
    """
    Получает файл от пользователя и делает его проверку "file_check".
    Если файл соотвествует, пробует сохранить.
    Если такой магазин уже есть ловит исключение и предупреждает пользователя.
    """
    items = await file_check(bot, message)
    if not items:
        return await waiting_for_file(bot, message)
    send_message = []
    for name, url, xpath in zip(*items):
        if not await db_parsing.create(name, url, xpath):
            await bot.send_message(
                message.chat.id, f"Имя - {name}, уже есть в базе данных"
            )
        average = await parser(url, xpath)
        send_message.append((
            f"name - {name}",
            f"url - {url}",
            f"xpath - {xpath}",
            f"Средняя стоймость зюзюблика - {average}"
        ))
    await file_send(bot, message, send_message)


if __name__ == '__main__':
    if TOKEN:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    else:
        print("Нет переменной TOKEN")
