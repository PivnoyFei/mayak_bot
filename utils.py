import csv
import os
import re
import uuid
from statistics import mean
from typing import List, Set, Union

import aiofiles
import pandas as pd
import requests
from aiogram import Bot
from aiogram.types import Message
from bs4 import BeautifulSoup as bs
from lxml import etree

from settings import FILES_DIR


async def generate_uuid() -> str:
    return str(uuid.uuid4().hex)


async def waiting_file(bot: Bot, message: Message, erorr: str = '') -> None:
    text = "Отправте файл в формате xlsx или csv. С полями - NAME, URL, XPATH"
    await bot.send_message(message.chat.id, erorr if erorr else text)


async def file_check(bot: Bot, message: Message) -> Union[tuple, None]:
    """Проверка формата файла и наличия колонок в нем."""
    if message.content_type == "document":
        size = message.document.file_name.split(".")[-1].lower()
        if size not in ("csv", "xlsx"):
            await waiting_file(bot, message, "Неверный формат файла")

        src = FILES_DIR / f"{await generate_uuid()}.{size}"
        try:
            await message.document.download(destination_file=src)
            read_file = {"xlsx": pd.read_excel, "csv": pd.read_csv}
            data = read_file[size](src)
            return data["NAME"], data["URL"], data["XPATH"]
        except Exception as e:
            await waiting_file(bot, message, f"Нет колонки {e}")
        finally:
            os.remove(src)
    else:
        await waiting_file(bot, message)
    return None


async def file_send(bot: Bot, message: Message, send_message: List) -> None:
    """Создает файл и результатами парсинга и отправляет пользователю."""
    src = FILES_DIR / f"{await generate_uuid()}.csv"
    try:
        with open(src, "wt", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerows(send_message)
        async with aiofiles.open(src, 'rb') as file:
            await bot.send_document(message.chat.id, file)
    except TypeError:
        await bot.send_message(
            message.chat.id, "Произошла ошибка при отправке файла"
        )
    finally:
        os.remove(src)


async def parser(url: str, xpath: str) -> int:
    response = requests.get(url, headers={'Content-Type': 'text/html', })
    response = bs(response.text, 'html.parser')
    dom = etree.HTML(str(response))
    set_nums: Set = {
        ("".join(re.findall(r'\b\d+\b', i))) for i in dom.xpath(xpath)
    }
    set_nums = {int(i) for i in set_nums if i.isdigit()}
    return round(mean(set_nums))
