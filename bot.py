import os
import logging
from aiogram import Bot, Dispatcher, executor, types

# =========================
# CONFIG
# =========================
API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# =========================
# START
# =========================
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📞 Contact info", "📝 Request a quote")

    await message.answer(
        "👋 Welcome to Easy AMZ!\n\n"
        "📦 Professional Amazon FBA & 3PL services in Canada\n\n"
        "We help sellers with:\n"
        "• Warehousing\n"
        "• FBA prep & labeling\n"
        "• Bundling & repackaging\n"
        "• Domestic & international shipping\n\n"
        "Choose an option below 👇",
        reply_markup=keyboard
    )

# =========================
# CONTACT INFO
# =========================
@dp.message_handler(lambda m: m.text == "📞 Contact info")
async def contact_info(message: types.Message):
    await message.answer(
        "📍 Locations:\n\n"
        "🇨🇦 Ontario (Fulfillment Center)\n"
        "Paris, ON\n\n"
        "63 Woodslee Ave, Unit A, N3L 3N6\n"
        "📞 Phone: +1 226 577 9352\n"
        "📧 Email:toronto@easyamz.ca\n\n"

        "🇨🇦 Cochrane, AB (Fulfillment Center)\n"
        "11-41070 Cook Rd, T4C 3A2\n"
        "📞 Phone: +1 825 967 5340\n"
        "📧 Email: hello@easyamz.ca\n\n"
        "🌐 Website: https://easyamz.ca"
    )

# =========================
# REQUEST A QUOTE
# =========================
@dp.message_handler(lambda m: m.text == "📝 Request a quote")
async def request_quote(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("📱 Send phone number", request_contact=True))
    kb.add("⬅️ Back")

    await message.answer(
        "Great! To get a quick quote, please share one of the following 👇\n\n"
        "• 📱 Your phone number (recommended)\n"
        "• 📧 Your email\n"
        "• ✍️ A short message describing your request\n\n"
        "An Easy AMZ specialist will contact you shortly.",
        reply_markup=kb
    )

# =========================
# PHONE RECEIVED
# =========================
@dp.message_handler(content_types=types.ContentType.CONTACT)
async def phone_received(message: types.Message):
    phone = message.contact.phone_number
    name = message.from_user.full_name
    username = f"@{message.from_user.username}" if message.from_user.username else "—"

    await bot.send_message(
        ADMIN_ID,
        "🔥 NEW 3PL LEAD\n\n"
        f"Name: {name}\n"
        f"Username: {username}\n"
        f"Phone: {phone}\n\n"
        "Source: Telegram Bot"
    )

    await message.answer(
        "✅ Thank you for contacting Easy AMZ!\n\n"
        "We’ve received your request.\n"
        "Our team will get back to you shortly during business hours.\n\n"
        "Have a great day!",
        reply_markup=types.ReplyKeyboardRemove()
    )

# =========================
# BACK TO MENU
# =========================
@dp.message_handler(lambda m: m.text == "⬅️ Back")
async def back_to_menu(message: types.Message):
    await start(message)

# =========================
# TEXT MESSAGE (EMAIL / DETAILS)
# =========================
@dp.message_handler()
async def text_message(message: types.Message):
    name = message.from_user.full_name
    username = f"@{message.from_user.username}" if message.from_user.username else "—"

    await bot.send_message(
        ADMIN_ID,
        "🔥 NEW 3PL LEAD\n\n"
        f"Name: {name}\n"
        f"Username: {username}\n"
        "Message:\n"
        f"{message.text}\n\n"
        "Source: Telegram Bot"
    )

    await message.answer(
        "✅ Thank you for contacting Easy AMZ!\n\n"
        "We’ve received your request.\n"
        "Our team will get back to you shortly during business hours.\n\n"
        "Have a great day!",
        reply_markup=types.ReplyKeyboardRemove()
    )

# =========================
# RUN
# =========================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
