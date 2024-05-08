from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import (
    orm_add_product,
    orm_get_products,
    orm_delete_product,
    orm_get_product,
    orm_update_product
)
from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.inline import get_callback_btns
from keyboards.reply import get_keyboard


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdmin())


ADMIN_KB = get_keyboard(
    'Добавить товар',
    'Ассортимент',
    placeholder='Выберите действие',
    sizes=(2,),
)


# Класс определения свойств для FSM
class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    product_for_change = None

    texts = {
        'AddProduct:name': 'Введите название заново',
        'AddProduct:description': 'Введите описание заново',
        'AddProduct:price': 'Введите стоимость заново',
        'AddProduct:image': 'Этот шаг последний...',
    }


@admin_router.message(Command('admin'))
async def add_product(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


@admin_router.message(F.text == "Ассортимент")
async def starring_at_product(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f'<strong>{product.name}\
                    </strong>\n{product.description}\nСтоимость: '
                    f'{round(product.price,2)}',
            parse_mode=ParseMode.HTML,
            reply_markup=get_callback_btns(
                btns={
                    'Удалить': f'delete_{product.id}',
                    'Изменить': f'change_{product.id}',
                }
            )
        )
    await message.answer("ОК, вот список товаров")


@admin_router.callback_query(F.data.startswith('delete_'))
async def delete_product(callback: types.CallbackQuery, session: AsyncSession):

    product_id = int(callback.data.split('_')[-1])
    await orm_delete_product(session, product_id)

    await callback.answer('Товар удален')
    await callback.message.answer('Товар удален!', parse_mode=ParseMode.HTML)


# FSM
@admin_router.callback_query(StateFilter(None), F.data.startswith('change_'))
async def change_product_callback(
        callback: types.CallbackQuery,
        session: AsyncSession,
        state: FSMContext,
        ):
    product_id = callback.data.split("_")[-1]

    product_for_change = await orm_get_product(session, int(product_id))

    AddProduct.product_for_change = product_for_change

    await callback.answer()
    await callback.message.answer(
        'Введите название товара', reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)


@admin_router.message(StateFilter(None), F.text == "Добавить товар")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название товара",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.set_state(AddProduct.name)


# Хендлер отмены и сброса состояния.
@admin_router.message(StateFilter('*'), Command('Отмена'))
@admin_router.message(StateFilter('*'), F.text.casefold() == 'отмена')
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return
    if AddProduct.product_for_change:
        AddProduct.product_for_change = None

    await state.clear()
    await message.answer('Действия отменены', reply_markup=ADMIN_KB)


# Хендлер команды назад (вернуться в предидущее состояние).
@admin_router.message(StateFilter('*'), Command("назад"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()

    if current_state == AddProduct.name:
        await message.answer(
            'Предидущего шага нет, либо введите назавние '
            'товара, либо напишите "Отмена"'
        )
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                f"Ок, вы вернулись к прошлому шагу \n"
                f"{AddProduct.texts[previous.state]}"
            )
            return
        previous = step


# Ловим текст для состояния name и меняем его на description.
@admin_router.message(AddProduct.name, or_f(F.text, F.text == '.'))
async def add_name(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(name=AddProduct.product_for_change.name)
        print(str(AddProduct.product_for_change))
    else:
        if len(message.text) >= 30:
            await message.answer(
                'Название товара не должно превышать 30 символов.'
                '\nВведите заново!',
                parse_mode=ParseMode.HTML

            )
            return
        await state.update_data(name=message.text)
    await message.answer("Введите описание товара")
    await state.set_state(AddProduct.description)


# Ловим некорректные вводы типов данных.
@admin_router.message(AddProduct.name)
async def add_name(message: types.Message, state: FSMContext):
    await message.answer(
        "Вы ввели недопустимые данные, введите текст название товара"
    )


# Ловим текст для состояния description и меняем его на price.
@admin_router.message(AddProduct.description, or_f(F.text, F.text == '.'))
async def add_description(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(
            description=AddProduct.product_for_change.description
        )
    else:
        await state.update_data(description=message.text)
    await message.answer("Введите стоимость товара")
    await state.set_state(AddProduct.price)


# Ловим некорректные вводы типов данных.
@admin_router.message(AddProduct.description)
async def add_description(message: types.Message, state: FSMContext):
    await message.answer(
        "Вы ввели недопустимые данные, введите текст описания товара"
    )


# Ловим текст для состояния price и меняем его на image.
@admin_router.message(AddProduct.price, or_f(F.text, F.text == ','))
async def add_price(message: types.Message, state: FSMContext):
    if message.text == ',':
        await state.update_data(price=AddProduct.product_for_change.price)
    else:
        try:
            float(message.text)
        except ValueError:
            await message.answer("Введите корректное значение цены")
            return

        await state.update_data(price=message.text)
    await message.answer("Загрузите изображение товара")
    await state.set_state(AddProduct.image)


# Ловим некорректные вводы типов данных.
@admin_router.message(AddProduct.price)
async def add_price(message: types.Message, state: FSMContext):
    await message.answer(
        "Вы ввели недопустимые данные, введите стоимость товара"
    )


# Ловим данные для состояние image и потом выходим из состояний
@admin_router.message(AddProduct.image, or_f(F.photo, F.text == '.'))
async def add_image(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession
):
    if message.text == '.':
        await state.update_data(image=AddProduct.product_for_change.image)
    else:
        await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    try:
        if AddProduct.product_for_change:
            await orm_update_product(
                session,
                AddProduct.product_for_change.id,
                data
            )
            await message.answer("Товар изменен", reply_markup=ADMIN_KB)
        else:
            await orm_add_product(session, data)
            await message.answer("Товар добавлен", reply_markup=ADMIN_KB)
        #  await message.answer(str(data), parse_mode=ParseMode.HTML)
        await state.clear()

    except Exception as e:
        await message.answer(
            f'Ошибка: \n{str(e)}\nОбратитесь к администратору',
            parse_mode=ParseMode.HTML,
            reply_markup=ADMIN_KB
        )
        await state.clear()

    AddProduct.product_for_change = None


# Ловим некорректные вводы типов данных.
@admin_router.message(AddProduct.image)
async def add_image(message: types.Message, state: FSMContext):
    await message.answer(
        "Вы ввели недопустимые данные, пришлите фото товара"
    )
