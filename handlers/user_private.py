from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f

user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привет, я виртуальный помощник!')


@user_private_router.message(
    or_f(Command('menu'), (F.text.lower() == 'меню'))
)
async def echo(message: types.Message):
    await message.answer('Вот меню:')


@user_private_router.message(
    or_f(Command('about'), (F.text.lower() == 'о нас'))
)
async def echo(message: types.Message):
    await message.answer(
        '[Для заказа пишите в сообщения группы или Viber/ WhatsApp/ Telegram +79165033435📩]'
        '(https://vk.com/slastenabento?w=club218813029)',
        parse_mode='Markdown'
    )


@user_private_router.message(
    or_f(Command('reviews'), (F.text.lower() == 'отзывы'))
)
async def echo(message: types.Message):
    await message.answer(
        '[Ваши отзывы:]'
        '(https://vk.com/slastenabento?from=search&z=album-218813029_291663410)',
        parse_mode='Markdown'
    )


@user_private_router.message(
    or_f(Command('payment'),
         ((F.text.lower() == 'варианты оплаты')
         | (F.text.lower().contains('плат'))))
)
async def echo(message: types.Message):
    await message.answer('Варианты оплаты')


@user_private_router.message(
    or_f(Command('shipping'),
         ((F.text.lower() == 'варианты доставки')
          | (F.text.lower().contains('доставк'))))
)
async def echo(message: types.Message):
    await message.answer('Варианты доставки:')




