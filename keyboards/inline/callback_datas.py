from aiogram.utils.callback_data import CallbackData

main_menu_choice = CallbackData("main", "item_name")
result_menu_choice = CallbackData("result", "item_name")
contests_menu_choice = CallbackData("contests","item_name")

main_menu_cb = CallbackData("show_menu", "level", "category", "subcategory", "to_do", "item_id")


menu_cd = CallbackData("show_menu", "user_id", "level", "category", "item_id")
sing_item = CallbackData("sing", "user_id", "category", "item")
unsing_item = CallbackData("unsing", "user_id","category", "item")

