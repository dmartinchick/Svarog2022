"""Описание колбэков"""
from aiogram.utils.callback_data import CallbackData

main_menu_choice = CallbackData("level", "category_name")
result_menu_choice = CallbackData("result", "item_name")
contests_menu_choice = CallbackData("contests","item_name")

main_menu_cb = CallbackData("main_menu", "level", "category", "subcategory", "item_id")


menu_cd = CallbackData("show_menu", "user_id", "level", "category", "item_id")
sing_item = CallbackData("sing", "user_id", "category", "item")
unsing_item = CallbackData("unsing", "user_id","category", "item")
