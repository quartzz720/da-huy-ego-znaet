import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo
from aiogram.utils import executor
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from config import settings
from models import Base, User
from trx_wallet import create_wallet
from scheduler import scheduler, update_balances

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    db = next(get_db())
    user = db.query(User).filter_by(telegram_id=message.from_user.id).first()
    if not user:
        address, priv = create_wallet()
        user = User(
            telegram_id=message.from_user.id,
            trx_address=address,
            private_key=priv,
        )
        db.add(user)
        db.commit()
    text = 'Welcome! Your TRX address: {}'
    url = f"{settings.WEBAPP_URL}?id={message.from_user.id}"
    await message.answer(
        text.format(user.trx_address),
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('Open WebApp', web_app=WebAppInfo(url=url))
        ),
    )


@dp.message_handler(commands=['profile'])
async def profile_handler(message: types.Message):
    db = next(get_db())
    user = db.query(User).filter_by(telegram_id=message.from_user.id).first()
    if not user:
        await message.answer('Use /start first')
        return
    await message.answer(
        f'Balance: {user.balance:.2f} TRX\nIncome per min: {user.trx_per_min} TRX'
    )


async def on_startup(dispatcher):
    scheduler.start()
    scheduler.add_job(update_balances, 'interval', minutes=1, args=[next(get_db())])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
