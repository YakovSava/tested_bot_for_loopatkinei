from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

class Keyboards:
	main_keyboard = ReplyKeyboardMarkup(keyboard=[[
		KeyboardButton(text="Яндекс.карты"),
		KeyboardButton(text="Оплатить Yoomoney")],[
		KeyboardButton(text="Картинка"),
		KeyboardButton(text="A2")]
	], resize_keyboard=True)
	check_pay = lambda label: ReplyKeyboardMarkup(keyboard=[[
		KeyboardButton(text=f"Проверить оплату {label}")
	]], resize_keyboard=True)