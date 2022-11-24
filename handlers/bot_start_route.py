from aiogram import Router, types
from aiogram.types.message import Message
from aiogram.filters import Command
from keyboards.simple_row import make_row_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
router = Router()

class UserRegistration(StatesGroup):
    entering_name = State()
    entering_surname = State()
    entering_middlename = State()
    choosing_status = State()
    choosing_vuz = State()
    entering_vuz = State()
    choosing_fakultet = State()
    entering_fakultet = State()
    choosing_year = State()
    entering_phone = State()
    entering_email = State()
    entering_vk = State()
    choosing_having_rights = State()
    choosing_having_car = State()
    choosing_using_carsharing = State()
    finished = State()

@router.message(Command(commands=['start']))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer('Привет! Рады приветствовать тебя в ЭкоГильдии!')
    await message.answer('Напиши, пожалуйста информацию о себе, которая понадобится нам для создания именных '
                         'благодарственных писем, котируемых при подаче на ПГАС!')
    await message.answer('Пожалуйста, введите имя')
    await state.update_data(username=message.from_user.username, user_id=message.from_user.id, chat_id=message.chat.id)

    await state.set_state(UserRegistration.entering_name)

@router.message(UserRegistration.entering_name)
async def name_entered(message: Message, state: FSMContext):
    await state.update_data(name=message.text.lower())
    await message.answer(text='Введите фамилию', reply_markup=make_row_keyboard(['Назад']))
