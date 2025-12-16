import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "8362334727:AAEky-Giur9AcxTS0B01kqIwSaTO0A-mjK8"
ADMIN_ID = "@easyamz_bot"  # твой Telegram ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📞 Contact info", "📝 Leave a request")

    await message.answer(
        "👋 Welcome to Easy AMZ!\n\n"
        "📦 Amazon FBA & 3PL services in Canada\n\n"
        "Choose an option below 👇",
        reply_markup=keyboard
    )

@dp.message_handler(lambda m: m.text == "📞 Contact info")
async def contact_info(message: types.Message):
    await message.answer(
        "📍 Address: Paris, ON\n"
        "📞 Phone: +1 226 577 9352\n"
        "🌐 Website: https://easyamz.ca"
    )

@dp.message_handler(lambda m: m.text == "📝 Leave a request")
async def request_start(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("📱 Send phone number", request_contact=True))
    kb.add("⬅️ Back")

    await message.answer(
        "Please share your email/message 👇",
        reply_markup=kb
    )

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def phone_received(message: types.Message):
    phone = message.contact.phone_number

    await bot.send_message(
        ADMIN_ID,
        f"🔥 NEW LEAD\n"
        f"Name: {message.from_user.full_name}\n"
        f"Phone: {phone}"
    )

    await message.answer(
        "✅ Thank you!\nWe’ll contact you shortly.",
        reply_markup=types.ReplyKeyboardRemove()
    )

@dp.message_handler(lambda m: m.text == "⬅️ Back")
async def back_to_menu(message: types.Message):
    await start(message)

@dp.message_handler()
async def text_message(message: types.Message):
    await bot.send_message(
        ADMIN_ID,
        f"🔥 NEW LEAD\n"
        f"From: @{message.from_user.username}\n"
        f"Name: {message.from_user.full_name}\n"
        f"Message:\n{message.text}"
    )

    await message.answer(
        "✅ Thank you!\nWe’ll contact you shortly.",
        reply_markup=types.ReplyKeyboardRemove()
    )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
