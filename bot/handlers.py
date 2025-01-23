from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot_config import bot
from checker import check_device, get_services
from data import AsyncSessionLocal, Users
from loguru import logger
from sqlalchemy import select

router = Router()


class ServiceCallback(CallbackData, prefix="service"):
    name: str
    service: int


class IMEI(StatesGroup):
    name = State()


@logger.catch
@router.message(CommandStart())
async def command_start_handler(message: Message):
    tg_id = message.from_user.id
    markup = InlineKeyboardBuilder()

    async with AsyncSessionLocal() as session:
        async with session.begin():
            query = select(Users).where(Users.tg_id == tg_id)
            users = await session.execute(query)
            user = users.scalars().first()
    if user is not None and user.is_white is True:
        mess = "Добро пожаловать в IMEI чекер!"
        button = InlineKeyboardButton(text="Запрос IMEI", callback_data="IMEI")

    else:
        mess = "Привет! К сожалению, ты пока не можешь пользоваться ботом."
        button = InlineKeyboardButton(text="Пока!", callback_data="bue")
    markup.add(button)
    markup = markup.as_markup()
    await bot.send_message(message.chat.id, mess, reply_markup=markup)


@router.callback_query(lambda callback: callback.data == "IMEI")
async def choose_service(callback: CallbackQuery, state: FSMContext):
    services = await get_services()
    await state.set_state(IMEI.name)
    text = "Выбери сервис"
    markup = InlineKeyboardBuilder()
    for service in services:
        button = InlineKeyboardButton(
            text=f"{service['title']}: {service['price']}",
            callback_data=ServiceCallback(name="service",
                                          service=service["id"]).pack(),
        )
        markup.add(button)
    markup.adjust(1)
    markup = markup.as_markup()
    await callback.message.answer(text, reply_markup=markup)


@router.callback_query(ServiceCallback.filter())
async def send_imei(
    callback: CallbackQuery, callback_data: ServiceCallback, state: FSMContext
):
    await state.set_state(IMEI.name)
    await state.update_data(service=callback_data.service)

    text = "Отправь IMEI в поле ниже"
    await callback.message.answer(text)


@router.message(IMEI.name)
async def accept_imei(message: Message, state: FSMContext):
    deviceId = message.text
    service = await state.get_data()
    result = await check_device(deviceId, service["service"])
    markup = InlineKeyboardBuilder()
    button = InlineKeyboardButton(text="Запрос IMEI", callback_data="IMEI")
    markup.add(button)
    markup = markup.as_markup()
    await message.answer(result, reply_markup=markup)
    await state.clear()
