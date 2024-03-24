from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_wanderers_keyboard(wanderers: list):
    builder = InlineKeyboardBuilder()
    for index, film in enumerate(wanderers):
        builder.button(text=film.get('title'),
                       callback_data=f"wanderer_{index}")
    return builder.as_markup()

def build_wanderer_details_keyboard(url):
    builder = InlineKeyboardBuilder()
    #builder.button(text="Перейти за посиланням", url=url)
    builder.button(text="Перейти назад", callback_data="back")
   # builder.button(text="Перейти назад", callback_data="back")
    return builder.as_markup()

def build_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Перелік пам'яток", callback_data=f"monuments")
    builder.button(text="Додати нову пам'ятку", callback_data=f"monumentcreate")
    return builder.as_markup()
