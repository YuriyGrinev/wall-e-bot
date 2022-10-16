from email import message
import logging

from aiogram import Bot, Dispatcher, executor, types

import time

from config.config import API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["help", "start"])
async def alarm(message: types.Message):
    await message.answer("Hi!\nI'm Wall-E bot!\nSend me photo!")


@dp.message_handler(content_types=["photo"])
async def echo_photo(message: types.Message):
    response_photo = await save_photo(message)
    await message.answer_photo(response_photo, caption="Test caption photo")


async def save_photo(message: types.Message):
    file_info = await bot.get_file(message.photo[-1].file_id)
    new_photo = (await bot.download_file(file_info.file_path)).read()
    now_time = time.strftime("%Y%m%d%H%M%SS", time.gmtime())
    user_id = message.from_user.id
    with open(f"photos/{user_id}_{now_time}.jpg", "wb") as file:
        file.write(new_photo)
        file.close()

    return new_photo


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
