from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import re

# Твой Telegram Bot Token
BOT_TOKEN = "8442896861:AAEtW4ZqFuKgTSMh5cr_Q9Nt5dYdLRG6wdc"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Хранилище уже обработанных ваучеров
seen_vouchers = set()

@dp.message_handler()
async def handle_message(message: types.Message):
    if not message.text:
        return

    voucher_pattern = r"1w-[\w\d\-]+"
    entities = message.entities or []

    for entity in entities:
        if entity.type in ['pre', 'code', 'spoiler']:
            text = message.text[entity.offset: entity.offset + entity.length]
            if re.match(voucher_pattern, text):
                if text not in seen_vouchers:
                    seen_vouchers.add(text)
                    # Если ваучер новый — можно обработать или сохранить
                    return
                else:
                    return  # Повтор — ничего не делаем

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
