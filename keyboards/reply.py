from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardRemove
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder


start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Меню'),
            KeyboardButton(text='О нас'),
            KeyboardButton(text='Отзывы'),
        ],
        [
            KeyboardButton(text='Варианты оплаты'),
            KeyboardButton(text='Варианты доставки'),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Что Вас интересует?'
)

del_keyboard = ReplyKeyboardRemove()

start_keyboard2 = ReplyKeyboardBuilder()
start_keyboard2.add(
    KeyboardButton(text='Меню'),
    KeyboardButton(text='О нас'),
    KeyboardButton(text='Отзывы'),
    KeyboardButton(text='Варианты оплаты'),
    KeyboardButton(text='Варианты доставки'),
)
start_keyboard2.adjust(3, 2)

test_keyboard = ReplyKeyboardBuilder()
test_keyboard.add(
    KeyboardButton(
        text='Создать опрос',
        request_poll=KeyboardButtonPollType()),
    KeyboardButton(
        text='Отправить номер телефона',
        request_contact=True,
    ),
    KeyboardButton(
        text='Отправить локацию',
        request_location=True,
    )

)

