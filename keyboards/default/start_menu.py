"""Формирование клавиатуры главного меню"""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

menu = KeyboardButton(text="⠀Меню")
start_menu_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(menu)
