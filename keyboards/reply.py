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


def get_keyboard(
        *btns: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        request_poll: int = None,
        sizes: tuple[int] = (2,),
):
    """
        Parameters request_contact and request_location must be as indexes of
        btns args for buttons you need.
        Example:
        get_keyboard(
                "Меню",
                "О магазине",
                "Варианты оплаты",
                "Варианты доставки",
                "Отправить номер телефона"
                placeholder="Что вас интересует?",
                request_contact=4,
                sizes=(2, 2, 1)
            )
        """
    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))
        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        elif request_poll and request_poll == index:
            keyboard.add(
                KeyboardButton(
                    text=text,
                    request_poll=KeyboardButtonPollType(),
                )
            )
        else:
            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True,
        input_field_placeholder=placeholder
    )
