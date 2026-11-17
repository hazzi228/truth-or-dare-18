"""Бот-лаунчер для мини-аппа «Правда или Действие 18+».

Запуск:
    pip install -r requirements.txt
    set BOT_TOKEN=123:ABC          (PowerShell: $env:BOT_TOKEN="123:ABC")
    set WEBAPP_URL=https://<ваш-ник>.github.io/truth-or-dare-18/
    python bot.py
"""
import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    Message,
    WebAppInfo,
)

# Подхватываем настройки из bot/.env (файл не попадает в git)
_env = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_env):
    with open(_env, encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.strip().split("=", 1)
                os.environ.setdefault(k, v)

BOT_TOKEN = os.environ["BOT_TOKEN"]
WEBAPP_URL = os.environ["WEBAPP_URL"]  # обязательно https://

dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message) -> None:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="🔥 Играть", web_app=WebAppInfo(url=WEBAPP_URL))
        ]]
    )
    await message.answer(
        "🔞 <b>Правда или Действие 18+</b>\n\n"
        "Пикантная игра для двоих.\n"
        "3 уровня жара, очки, таймер и десятки заданий.\n\n"
        "Только для 18+. Любое задание можно пропустить.",
        reply_markup=kb,
    )


async def main() -> None:
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    # Кнопка «Играть» слева от поля ввода
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Играть", web_app=WebAppInfo(url=WEBAPP_URL))
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
