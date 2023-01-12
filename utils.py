import csv
import os
import re
import uuid
from statistics import mean

import aiofiles
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from lxml import etree

from settings import FILES_DIR


async def generate_uuid() -> str:
    return str(uuid.uuid4().hex)


async def waiting_for_file(bot, message, erorr: str = None) -> None:
    text = "Отправте файл в формате xlsx или csv. С полями - NAME, URL, XPATH"
    await bot.send_message(message.chat.id, erorr if erorr else text)


async def file_check(bot, message) -> tuple | None:
    """Проверка формата файла и наличия колонок в нем."""
    if message.content_type == "document":
        size = message.document.file_name.split(".")[-1].lower()
        if size not in ("csv", "xlsx"):
            await waiting_for_file(bot, message, "Неверный формат файла")

        src = FILES_DIR / f"{await generate_uuid()}.{size}"
        try:
            await message.document.download(destination_file=src)
            read_file = {"xlsx": pd.read_excel, "csv": pd.read_csv}
            data = read_file[size](src)
            return data["NAME"], data["URL"], data["XPATH"]
        except Exception as e:
            await waiting_for_file(bot, message, f"Нет колонки {e}")
        finally:
            os.remove(src)
    else:
        await waiting_for_file(bot, message)


async def file_send(bot, message, send_message: list) -> None:
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
    set_nums = {("".join(re.findall(r'\b\d+\b', i))) for i in dom.xpath(xpath)}
    set_nums = {int(i) for i in set_nums if i.isdigit()}
    return round(mean(set_nums))
