import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from dotenv import load_dotenv

# Загрузка .env
load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- Кнопки главного меню ---
menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
menu_kb.add("🛍 View Sneakers", "❓ Help")

# --- Каталог товаров ---
sneakers = [
    {"name": "Nike Air Max 90", "price": 119, "sizes": "38–44"},
    {"name": "New Balance 327", "price": 105, "sizes": "36–43"},
    {"name": "Yeezy 350 Bone", "price": 149, "sizes": "40–45"}
]

# --- Команда /start ---
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("👋 Welcome to SneakerDrops!\nBrowse our top drops and place your order directly here.", reply_markup=menu_kb)

# --- Обработка выбора кроссовок ---
@dp.message_handler(lambda message: message.text == "🛍 View Sneakers")
async def show_catalog(message: types.Message):
    for shoe in sneakers:
        btn = InlineKeyboardMarkup().add(
            InlineKeyboardButton(f"Order for ${shoe['price']}", callback_data=f"order:{shoe['name']}")
        )
        text = f"👟 <b>{shoe['name']}</b>\nSizes: {shoe['sizes']}\nPrice: ${shoe['price']}"
        await message.answer(text, parse_mode="HTML", reply_markup=btn)

# --- Обработка заказа ---
@dp.callback_query_handler(lambda call: call.data.startswith("order:"))
async def process_order(call: types.CallbackQuery):
    sneaker_name = call.data.split(":")[1]
    await bot.send_message(call.from_user.id,
        f"✅ Your order for <b>{sneaker_name}</b> is received!\n\n"
        "Please send payment of the listed amount to this wallet or card and reply here with the screenshot.\n\n"
        "💳 USDT TRC20: T9e...\n💳 Bank Card: **** 1234\n\n"
        "We’ll confirm your order shortly.",
        parse_mode="HTML"
    )
    await bot.send_message(int(ADMIN_ID),
        f"📥 New order: {sneaker_name}\nUser: @{call.from_user.username} (ID: {call.from_user.id})"
    )

# --- Помощь ---
@dp.message_handler(lambda message: message.text == "❓ Help")
async def help_msg(message: types.Message):
    await message.answer("Need assistance? Message @support_sneakerdrops or simply reply here.")

# --- Запуск ---
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
