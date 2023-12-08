import asyncio
import logging

import requests
import bs4
import lxml
from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart
import datetime

timetable_text = list()
def find_timetable(day_of_week, url):

    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "lxml")

    date_today = "day " + datetime.date.today().strftime('%A').lower()
    if (date_today == day_of_week):
        day_of_week += " today"

    block_day = soup.find("div", class_=day_of_week)

    if (block_day == None):
        return
    else:
        block_line = block_day.find_all("div", class_="line")

        timetable_text.append(day_of_week+'\n\n\n')

        for i in block_line:
            disc_time = i.find("div", class_="hidden-xs")
            subgroup = i.find("li", class_="bold num_pdgrp")

            if (subgroup != None):
                num_sub_group = i.find_all("div", class_="col-md-6.0")

                for j in num_sub_group:
                    disc_name = j.find("span", class_="name")
                    disc_location = j.find("a", href="#")
                    disc_subgroup = j.find("li", class_="bold num_pdgrp")

                    timetable_text.append(f'{disc_time.text.split()} {disc_name.text} [{disc_location.text}] - {disc_subgroup.text}\n')
            else:
                disc_name = i.find("span", class_="name")
                disc_location = i.find("a", href="#")
                disc_subgroup = i.find_all("li")[-1]

                timetable_text.append(f'{disc_time.text.split()} {disc_name.text} [{disc_location.text}] - {disc_subgroup.text}\n')
    timetable_text.append('\n\n')






BOT_TOKEN = "YOUR TOKEN"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def handler_start(message: types.Message):
    await message.answer(text=f"Привет, {message.from_user.full_name}! Ты можешь написать мне свою группу и я отправлю твоё расписание на всю рабочую неделю!")

@dp.message()
async def echo_message(message: types.Message):
    timetable_text_str = '\n'.join(timetable_text)
    await message.answer(
        text=timetable_text_str,
    )
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)










if __name__ == "__main__":

    url = "https://timetable.pallada.sibsau.ru/timetable/group/11726"

    # print("Понедельник")
    find_timetable(day_of_week="day monday", url=url)
    # print("Вторник")
    find_timetable(day_of_week="day tuesday", url=url)
    # print("Среда")
    find_timetable(day_of_week="day wednesday", url=url)
    # print("Четверг")
    find_timetable(day_of_week="day thursday", url=url)
    # print("Пятница")
    find_timetable(day_of_week="day friday", url=url)
    # print("Суббота")
    find_timetable(day_of_week="day saturday", url=url)

    asyncio.run(main())