from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import types

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
kb.row(button_1, button_2)
button_3 = KeyboardButton(text='Купить')
kb.add(button_3)
kb_inl = InlineKeyboardMarkup()
kb_inl2 = InlineKeyboardMarkup()
button_kb_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_kb_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
button_kb_3 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button_kb_4 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button_kb_5 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button_kb_6 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kb_inl.add(button_kb_1)
kb_inl.add(button_kb_2)
kb_inl2.add(button_kb_3)
kb_inl2.add(button_kb_4)
kb_inl2.add(button_kb_5)
kb_inl2.add(button_kb_6)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    images = ['image1.png', 'image2.png', 'image3.png', 'image4.png']
    captions = [
        'Название: Product 1 | Описание: описание 1 | Цена: 100',
        'Название: Product 2 | Описание: описание 2 | Цена: 200',
        'Название: Product 3 | Описание: описание 3 | Цена: 300',
        'Название: Product 4 | Описание: описание 4 | Цена: 400'
    ]

    for i in range(len(images)):
        with open(images[i], 'rb') as img:
            await message.answer_photo(img, caption=captions[i], parse_mode='Markdown')
    await message.answer('Выберите продукт для покупки:', reply_markup=kb_inl2)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=kb_inl)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Формула Миффлина-Сан Жеора: 10 * вес + 6.25 * рост - 5 * возраст - 161')



@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age_param=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth_param=message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight_param=message.text)
    data = await state.get_data()
    age = int(data['age_param'])
    growth = int(data['growth_param'])
    weight = int(data['weight_param'])
    calories = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(f'Ваша дневная норма калорий: {calories} ккал')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)