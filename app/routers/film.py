from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold
from typing import Union

from ..data import (
    get_wanderers,
    get_wanderer,
    save_wanderer
)

from ..keyboards import (
    build_wanderers_keyboard,
    build_wanderer_details_keyboard,
    build_menu_keyboard
)

from ..fsm import WandererCreateForm

from .Utils import edit_or_answer
wanderer_router = Router()

@wanderer_router.callback_query(F.data == "monuments")
@wanderer_router.message(Command("monuments"))
@wanderer_router.message(F.text.casefold() == "monuments")
async def show_wanderers_command(message: Union[CallbackQuery, Message], state: FSMContext) -> None:
    wanderers = get_wanderers()
    if isinstance(message, Message):
        if wanderers:
            keyboard = build_wanderers_keyboard(wanderers)
            await edit_or_answer(message, "Виберіть будь-яку пам'ятку", keyboard)
        else:
            await edit_or_answer(message,
             "Нажаль зараз відсутні пам'ятки. Спробуйте /monumentcreate для створення нової.",
              ReplyKeyboardRemove())
    elif isinstance(message, CallbackQuery):
        if wanderers:
            keyboard = build_wanderers_keyboard(wanderers)
            await edit_or_answer(
                message.message,
            "Виберіть будь-яку пам'ятку",
                 keyboard)
        else:
            await edit_or_answer(
                message.message,
          "Нажаль зараз відсутні пам'ятки. Спробуйте /monumentcreate для створення нової.")


@wanderer_router.message(Command("monumentcreate"))
@wanderer_router.callback_query(F.data == "monumentcreate")
@wanderer_router.message(F.text.casefold() == "monumentcreate")
@wanderer_router.message(F.text.casefold() == "create monument")
async def create_wanderer_command(message: Union[Message, CallbackQuery], state: FSMContext) -> None:
    await state.clear()
    await state.set_state(WandererCreateForm.title)
    await edit_or_answer(message, "Яка назва пам'ятки?", ReplyKeyboardRemove())


# from aiogram.utils.markdown import hbold
@wanderer_router.callback_query(F.data.startswith("wanderer_"))
async def show_wanderer_details(callback: CallbackQuery, state: FSMContext) -> None:
    wander_id = int(callback.data.split("_")[-1])
    wanderer = get_wanderer(wander_id)
    text = (f"Назва: {hbold(wanderer.get('title'))}\n"
            f"Опис: {hbold(wanderer.get('desc'))}"
            #f"Рейтинг: {hbold(film.get('rating'))}"
            )
    photo_id = wanderer.get('photo')
    url = wanderer.get('url')
    await callback.message.answer_photo(photo_id)
    await edit_or_answer(callback.message, text, build_wanderer_details_keyboard(url))


@wanderer_router.message(WandererCreateForm.title)
async def proces_title(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(WandererCreateForm.desc)
    await edit_or_answer(message, "Який опис пам'ятки?", ReplyKeyboardRemove())

@wanderer_router.message(WandererCreateForm.desc)
async def proces_description(message: Message, state: FSMContext) -> None:
    data = await state.update_data(desc=message.text)
    await state.set_state(WandererCreateForm.url)
    await edit_or_answer(
        message,
        f"Введіть місцезнаходження пам'ятки: {hbold(data.get('title'))}",
        ReplyKeyboardRemove(),
    )

@wanderer_router.message(WandererCreateForm.url)
@wanderer_router.message(F.text.contains('http'))
async def procees_url(message: Message, state: FSMContext) -> None:
    data = await state.update_data(url=message.text)
    await state.set_state(WandererCreateForm.photo)
    await edit_or_answer(
        message,
        f"Надайте фото пам'ятки: {hbold(data.get('title'))}",
        ReplyKeyboardRemove(),
    )

@wanderer_router.message(WandererCreateForm.photo)
@wanderer_router.message(F.photo)
async def proces_photo(message: Message, state: FSMContext) -> None:
    photo = message.photo[-1]
    photo_id = photo.file_id

    data = await state.update_data(photo=photo_id)
    await state.clear()
    save_wanderer(data)
    return await show_wanderers_command(message, state)

@wanderer_router.callback_query(F.data == "back")
@wanderer_router.message(Command("back"))
async def back_handler(callback: Union[CallbackQuery, Message], state: FSMContext) -> None:
    await state.clear()
    return await show_wanderers_command(callback.message, state)
