from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# keyboard for callback buttons
def get_callback_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,)
    ):

    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
    return keyboard.adjust(*sizes).as_markup()


# keyboard for url buttons
def get_url_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,)
        ):

    keyboard = InlineKeyboardBuilder()

    for text, url in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, url=url))
    return keyboard.adjust(*sizes).as_markup()


# keyboard universal for callback and url buttons
def get_universal_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,)
        ):
    keyboard = InlineKeyboardBuilder()

    for text, value in btns.items():
        if value.startswith('http') or '://' in value:
            keyboard.add(InlineKeyboardButton(text=text, url=value))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=value))
        return keyboard.adjust(*sizes).as_markup()
