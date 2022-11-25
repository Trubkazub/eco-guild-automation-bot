from aiogram import Router, types
from aiogram.types.message import Message
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from keyboards.simple_row import make_row_keyboard, make_keyboard_column
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()
available_statuses = ['Учащийся в школе', 'Студент', 'Выпускник']


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
    await message.answer('Пожалуйста, введите имя', reply_markup=None)
    await state.update_data(username=message.from_user.username, user_id=message.from_user.id, chat_id=message.chat.id)
    await state.set_state(UserRegistration.entering_name)


@router.message(UserRegistration.entering_name)
async def name_entered(message: Message, state: FSMContext):
    await state.update_data(name=message.text.lower())
    await message.answer(text='Введите фамилию', reply_markup=make_row_keyboard(['Назад']))
    await state.set_state(UserRegistration.entering_surname)

@router.message(UserRegistration.entering_surname, Text(text='Назад'))
async def surname_back(message: Message, state: FSMContext):
    await state.update_data(name='')
    await state.set_state(UserRegistration.entering_name)
    await message.answer('Введите имя')

@router.message(UserRegistration.entering_surname)
async def surname_entered(message: Message, state: FSMContext):
    await state.update_data(surname=message.text.lower())
    await message.answer(text='Введите отчество', reply_markup=make_row_keyboard(['Назад']))
    await state.set_state(UserRegistration.entering_middlename)

@router.message(UserRegistration.entering_middlename, Text(text='Назад'))
async def middlename_back(message: Message, state: FSMContext):
    await state.update_data(name='')
    await state.set_state(UserRegistration.entering_surname)
    await message.answer('Введите фамилию')

@router.message(UserRegistration.entering_middlename)
async def middlename_entered(message: Message, state: FSMContext):
    await state.update_data(middlname=message.text.lower())
    await message.answer(text='Выберите ваш статус', reply_markup=make_keyboard_column(available_statuses))
    await state.set_state(UserRegistration.choosing_status)



@router.message(UserRegistration.choosing_status, Text(text=available_statuses))
async def choosing_status(message: Message, state: FSMContext):
    await state.update_data(status=message.text)
    await message.answer(text='Отлично. Проверяем')

