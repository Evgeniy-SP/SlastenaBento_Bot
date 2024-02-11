from string import punctuation

from aiogram import F, types, Router

user_group_router = Router()

restricted_words = {'мудак', 'баран', 'ишак'}


def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))

@user_group_router.message()
async def cleaner(message: types.Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f'{message.from_user.first_name}, соблюдайте порядок в чате!')
        await message.delete()
        # await message.chat.ban(message.from_user.id)
