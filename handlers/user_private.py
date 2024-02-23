from aiogram import types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.formatting import as_marked_section, Bold

from filters.chat_types import ChatTypeFilter
from keyboards import reply

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        'Привет, я виртуальный помощник',
        reply_markup=reply.start_keyboard2.as_markup(
            resize_keyboard=True,
            input_field_placeholder='Что Вас интересует?',
        ),
    )


@user_private_router.message(
    or_f(Command('menu'), (F.text.lower() == 'меню'))
)
async def echo(message: types.Message):
    await message.answer(
        'Вот меню:',
        reply_markup=reply.test_keyboard.as_markup(
            resize_keyboard=True,
            input_field_placeholder='Что Вас интересует?',
        ),
    )


@user_private_router.message(
    or_f(Command('about'), (F.text.lower() == 'о нас'))
)
async def echo(message: types.Message):
    await message.answer(
        '[Для заказа пишите в сообщения группы или Viber/ WhatsApp/ Telegram 79165033435📩]'
        '(https://vk.com/slastenabento?w=club218813029)'
    )


@user_private_router.message(
    or_f(Command('reviews'), (F.text.lower() == 'отзывы'))
)
async def echo(message: types.Message):
    await message.answer(
        '[Ваши отзывы:]'
        '(https://vk.com/slastenabento?from=search&z=album-218813029_291663410)'
    )


@user_private_router.message(
    or_f(Command('payment'),
         ((F.text.lower() == 'варианты оплаты')
         | (F.text.lower().contains('плат'))))
)
async def echo(message: types.Message):
    text = as_marked_section(
        Bold('Варианты оплаты:'),
        'Картой онлайн',
        'При получении карта / наличные',
        marker='✅ '
    )
    await message.answer(text.as_markdown())


@user_private_router.message(
    or_f(Command('shipping'),
         ((F.text.lower() == 'варианты доставки')
          | (F.text.lower().contains('доставк'))))
)
async def echo(message: types.Message):
    text = as_marked_section(
        Bold('Варианты доставки:'),
        'Самовывоз',
        'Доставка курьером',
        marker='✅ '
    )
    await message.answer(text.as_markdown())


@user_private_router.message(F.contact)
async def get_contact(message: types.Message):
    await message.answer(
        f'номер получен: {message.contact.phone_number}',
        parse_mode=ParseMode.HTML
    )
    await message.answer(str(message.contact), parse_mode=ParseMode.HTML)


@user_private_router.message(F.location)
async def get_location(message: types.Message):
    await message.answer(f'локация получена')
    await message.answer(str(message.location), parse_mode=ParseMode.HTML)




