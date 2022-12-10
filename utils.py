import os
import re
from statistics import mean

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from lxml import etree

from settings import FILES_DIR


def waiting_for_file(bot, message, erorr=None) -> None:
    text = "Отправте файл в формате csv. С полями - NAME, URL, XPATH"
    bot.reply_to(message, erorr if erorr else text)


def file_check(bot, message) -> tuple | None:
    """Проверка формата файла и наличия колонок в нем."""
    if message.content_type == "document":
        name = message.from_user.username
        file_info = bot.get_file(message.document.file_id)

        size = message.document.file_name.split(".")[-1].lower()
        if size not in ("csv", "xlsx"):
            waiting_for_file(bot, message, "Неверный формат файла")

        src = FILES_DIR / f"{name}.{size}"
        try:
            with open(src, "wb") as file:
                file.write(bot.download_file(file_info.file_path))
            read_file = {"xlsx": pd.read_excel, "csv": pd.read_csv}
            data = read_file[size](src)
            return data["NAME"], data["URL"], data["XPATH"]
        except Exception as e:
            waiting_for_file(bot, message, f"Нет колонки {e}")
        finally:
            os.remove(src)
    else:
        waiting_for_file(bot, message)


def parser(url: str, xpath: str) -> int:
    response = requests.get(url, headers={'Content-Type': 'text/html', })
    response = bs(response.text, 'html.parser')
    dom = etree.HTML(str(response))
    set_nums = {("".join(re.findall(r'\b\d+\b', i))) for i in dom.xpath(xpath)}
    set_nums = {int(i) for i in set_nums if i.isdigit()}
    return round(mean(set_nums))
