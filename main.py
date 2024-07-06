from time import strptime
from asyncio import run
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.enums import ParseMode
from aiogram.filters.command import Command

from plugins.keyboards import Keyboards
from plugins.payeer import Yoomoney
from plugins.goodrive import Sheet
from plugins.getter import OPTIMIZED

if OPTIMIZED:
	from plugins.getter import OptimizedGetter as Getter
else:
	from plugins.getter import NonOptimizedGetter as Getter
from plugins.getter import TomlGetter

getter = Getter()
tomler = TomlGetter(getter=getter)
startup_config = tomler.load('config.ini')
sheets = Sheet(cred_filename=startup_config['credentials'])
pay = Yoomoney({
	'token': startup_config['yoomoney'],
	'account': startup_config['account']
})

bot = Bot(token=startup_config['token'])
dp = Dispatcher()

@dp.message(Command('start'))
async def start_handler(message:Message):
	await message.answer('Привет! Вот клавиатура!', reply_markup=Keyboards.main_keyboard)

@dp.message(F.text == "Яндекс.карты")
async def yandex_maps(message:Message):
	await message.answer('Россия, Свердловская область, Г. Берёзовский, Ул. Ленина 1\n\nhttps://yandex.ru/maps/29397/berezovskyi/house/ulitsa_lenina_1/YkkYcQ9hTEEPQFtsfXVxdnlkZw==/?ll=60.781548%2C56.907573&z=16')
	await message.answer('Но возможно вам нужна была локация?')
	await bot.send_location(
		chat_id=message.from_user.id,
		latitude=56.907573,
		longitude=60.781548
	)

@dp.message(F.text == "Оплатить Yoomoney")
async def yoomoney_handler(message:Message):
	link, label = pay.build_quickpay(2)
	await message.answer(f'Ссылка для оплаты 2р\nПлатёжная система Yoomoney\nСсылка: {link}\n\nПосле оплаты нажмите на кнопку', reply_markup=Keyboards.check_pay(label))

@dp.message(F.text.startswith("Проверить оплату "))
async def check_pay_handler(message:Message):
	if message.text.split()[-1] == 'оплату':
		await message.answer('Не пытайтесь обмануть бота!')
	else:
		if pay.check_pay(message.text.split()[-1]):
			await message.answer('Вы успешно оплатили 2руб!', reply_markup=Keyboards.main_keyboard)
		else:
			await message.answer('Извините, но оплата не прошла. Попробуйте нажать снова на кнопку')

@dp.message(F.text == "A2")
async def a2_handler(message:Message):
	await message.answer(f'Данные ячейки A2 - {sheets.read_cell("A2")}')

@dp.message(F.text == "Картинка")
async def image_send(message:Message):
	photo = FSInputFile('./image.jpg')
	await bot.send_photo(
		chat_id=message.from_user.id,
		photo=photo,
		caption='Картинка!'
	)

@dp.message()
async def none_handler(message:Message):
	try:
		strptime(message.text, '%d.%m.%Y')
	except Exception as ex:
		print(ex)
		await message.answer('Неверная дата!')
	else:
		cell = int(getter.read('last_cell.txt'))
		sheets.update_cell(f"A{cell}", str(message.from_user.id))
		sheets.update_cell(f"B{cell}", message.text)
		getter.write('last_cell.txt', str(cell+1))
		await message.answer('Дата верна!')

if __name__ == '__main__':
	print('Start!')
	run(dp.run_polling(bot))