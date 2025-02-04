import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import LabeledPrice, PreCheckoutQuery

# Настройки (ТЕСТОВЫЕ!)
API_TOKEN = "5000473503:AAEgrgzmUqXbs3JIH0rRWl0oiv3eq7gCUsU/test"  # Тестовый токен
PAYMENT_PROVIDER_TOKEN = "TEST:5000473503"  # Тестовый платежный токен
OWNER_ID = 123456789  # Замени на свой Telegram ID

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# База данных (имитация)
user_balance = {}


# Команда: Пополнить баланс (ТЕСТОВАЯ!)
@dp.message(commands=["pay"])
async def send_invoice(message: types.Message):
    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        await message.reply("Укажи сумму в звездах: /pay 50")
        return

    amount = int(args[1])
    if amount <= 0:
        await message.reply("Сумма должна быть больше 0!")
        return

    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Пополнение (ТЕСТ)",
        description=f"Тестовое пополнение на {amount} звезд",
        payload=str(amount),
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency="USD",
        prices=[LabeledPrice(label="Тестовые звезды", amount=amount * 100)],
        start_parameter="test_payment",
        provider_data=None,
        send_email_to_provider=False
    )


# Обработка успешного тестового платежа
@dp.pre_checkout_query(lambda q: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message(lambda message: message.successful_payment)
async def process_successful_payment(message: types.Message):
    user_id = message.from_user.id
    amount = int(message.successful_payment.total_amount / 100)

    # Обновляем тестовый баланс
    user_balance[user_id] = user_balance.get(user_id, 0) + amount

    await message.reply(f"✅ ТЕСТОВЫЙ баланс пополнен на {amount} звезд!\n💰 Баланс: {user_balance[user_id]} звезд")


# Команда: Спам подарками (ТОЛЬКО ТЕСТОВЫЙ СЕРВЕР!)
@dp.message(commands=["spam"])
async def send_gifts(message: types.Message):
    if message.from_user.id != OWNER_ID:
        await message.reply("⛔ Только владелец бота может использовать эту команду!")
        return

    args = message.text.split()
    count = int(args[1]) if len(args) > 1 and args[1].isdigit() else 10  # Количество тортов по умолчанию

    await message.reply(f"🎂 Начинаю тестовый спам подарками ({count} шт.)")

    for i in range(count):
        await bot.send_message(OWNER_ID, "🎂 [ТЕСТ] Тебе тестовый подарок!")
        await asyncio.sleep(1)  # Задержка, чтобы Telegram не банил


# Проверка, что запущен ТОЛЬКО тестовый сервер
if "/test" not in API_TOKEN:
    raise RuntimeError("❌ БОТ ДОЛЖЕН РАБОТАТЬ ТОЛЬКО НА ТЕСТОВОМ СЕРВЕРЕ!")

# Бесконечный цикл для работы на Amvera
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())  # Поддержка работы бота 24/7
