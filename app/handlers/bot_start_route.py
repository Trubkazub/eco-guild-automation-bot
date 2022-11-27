from aiogram import Router, types
from aiogram.types.message import Message
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from keyboards.simple_row import make_row_keyboard, make_keyboard_column
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup

router = Router()
available_statuses = ['Учащийся в школе', 'Студент', 'Выпускник']
available_vuzes = ['МГУ', 'Другой']
yes_no_buttons = ['Да', 'Нет']
available_fakultets = ['Биологический факультет', 'Биотехнологический факультет', 'Высшая школа бизнеса', 'Высшая школа государственного администрирования', 'Высшая школа государственного аудита', 'Высшая школа инновационного бизнеса', 'Высшая школа культурной политики и управления в гуманитарной сфере', 'Высшая школа перевода', 'Высшая школа современных социальных наук', 'Высшая школа телевидения', 'Высшая школа управления и инноваций', 'Географический факультет', 'Геологический факультет', 'Институт стран Азии и Африки', 'Исторический факультет', 'Механико–математический факультет', 'Московская школа экономики', 'Социологический факультет', 'Факультет биоинженерии и биоинформатики', 'Факультет вычислительной математики и кибернетики', 'Факультет глобальных процессов', 'Факультет государственного управления', 'Факультет журналистики', 'Факультет иностранных языков и регионоведения', 'Факультет искусств', 'Факультет космических исследований', 'Факультет мировой политики', 'Факультет наук о материалах', 'Факультет педагогического образования', 'Факультет политологии', 'Факультет почвоведения', 'Факультет психологии', 'Факультет фундаментальной медицины', 'Факультет фундаментальной физико-химической инженерии', 'Физический факультет', 'Филологический факультет', 'Философский факультет', 'Химический факультет', 'Экономический факультет', 'Юридический факультет']
available_years = ['I курс бакалавриата', 'II курс бакалавриата', 'III курс бакалавриата', 'IV курс бакалавриата', 'I курс магистратуры', 'II курс магистратуры', 'I курс специалитета', 'II курс специалитета', 'III курс специалитета', 'IV курс специалитета', 'V курс специалитета', 'VI курс специалитета', 'I курс аспирантуры', 'II курс аспирантуры', 'III курс аспирантуры', 'IV курс аспирантуры']

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
    choosing_autovolonteur = State()
    choosing_having_rights = State()
    choosing_having_car = State()
    choosing_using_carsharing = State()
    finished = State()


@router.message(Command(commands=['start']))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer('Привет! Рады приветствовать тебя в ЭкоГильдии!')
    await message.answer('Напиши, пожалуйста информацию о себе, которая понадобится нам для создания именных '
                         'благодарственных писем, котируемых при подаче на ПГАС!')
    await message.answer('Пожалуйста, введите имя', reply_markup=ReplyKeyboardMarkup)
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
    await message.answer('Введите имя')
    await state.set_state(UserRegistration.entering_name)

@router.message(UserRegistration.entering_surname)
async def surname_entered(message: Message, state: FSMContext):
    await state.update_data(surname=message.text.lower())
    await message.answer(text='Введите отчество', reply_markup=make_row_keyboard(['Назад']))
    await state.set_state(UserRegistration.entering_middlename)

@router.message(UserRegistration.entering_middlename, Text(text='Назад'))
async def middlename_back(message: Message, state: FSMContext):
    await state.update_data(name='')
    await message.answer('Введите фамилию')
    await state.set_state(UserRegistration.entering_surname)

@router.message(UserRegistration.entering_middlename)
async def middlename_entered(message: Message, state: FSMContext):
    await state.update_data(middlname=message.text.lower())
    await message.answer(text='Выберите ваш статус', reply_markup=make_keyboard_column(available_statuses))
    await state.set_state(UserRegistration.choosing_status)



@router.message(UserRegistration.choosing_status, Text(text=available_statuses))
async def choosed_status(message: Message, state: FSMContext):
    await state.update_data(status=message.text)
    if message.text == available_statuses[1]:
        await message.answer(text='Выберите ВУЗ', reply_markup=make_keyboard_column(available_vuzes))
        await state.set_state(UserRegistration.choosing_vuz)
    else:
        await message.answer(text='Введите номер телефона')
        await state.set_state(UserRegistration.entering_phone)

@router.message(UserRegistration.choosing_status)
async def choosed_wrong_status(message: Message, state: FSMContext):
    await message.answer('Пожалуйста, выберите статус из списка')

@router.message(UserRegistration.choosing_vuz)
async def choosed_vuz(message: Message, state: FSMContext):
    if message.text in available_vuzes:
        if message.text == available_vuzes[0]:
            await state.update_data(vuz=message.text.lower())
            await message.answer(text='Пожалуйста выберите факультет', reply_markup=make_keyboard_column(available_fakultets))
            await state.set_state(UserRegistration.choosing_fakultet,)
        else:
            await message.answer(text='Пожалуйста введите название ВУЗа', reply_markup=None)
            await state.set_state(UserRegistration.entering_vuz)
    else:
        await state.update_data(vuz=message.text.lower())
        await message.answer(text='Пожалуйста введите ваш факультет', reply_markup=None)
        await state.set_state(UserRegistration.entering_fakultet)

@router.message(UserRegistration.entering_vuz)
async def entered_vuz(message: Message, state: FSMContext):
    await state.update_data(vuz=message.text)
    await message.answer('Введите факультет', reply_markup=None)
    await state.set_state(UserRegistration.entering_fakultet)

@router.message(UserRegistration.choosing_fakultet, Text(text=available_fakultets))
async def choosed_fakultet(message: Message, state: FSMContext):
    await state.update_data(fakultet=message.text)
    await message.answer('Выберите год обучения', reply_markup=make_keyboard_column(available_years))
    await state.set_state(UserRegistration.choosing_year)

@router.message(UserRegistration.choosing_fakultet)
async def choosed_wrong_fakultet(message: Message, state: FSMContext):
    await message.answer('Пожалуйста выберите факультет из списка')

@router.message(UserRegistration.choosing_year, Text(text=available_years))
async def choosed_year(message: Message, state: FSMContext):
    await state.update_data(year=message.text)
    await message.answer('Введите номер телефона')
    await state.set_state(UserRegistration.entering_phone)

@router.message(UserRegistration.choosing_year)
async def choosed_wrong_year(message: Message, state: FSMContext):
    await message.answer('Пожалуйста выберите год обучения из списка')

@router.message(UserRegistration.entering_phone)
async def entered_phone(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer('Введите электронную почту')
    await state.set_state(UserRegistration.entering_email)

@router.message(UserRegistration.entering_email)
async def entered_phone(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer('Введите ссылку на профиль ВК')
    await state.set_state(UserRegistration.entering_vk)

@router.message(UserRegistration.entering_email)
async def entered_phone(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer('Введите ссылку на профиль ВК')
    await state.set_state(UserRegistration.entering_vk)

@router.message(UserRegistration.entering_vk)
async def entered_phone(message: Message, state: FSMContext):
    await state.update_data(vk=message.text)
    await message.answer(text='Можете ли вы стать потенциальным автоволонтёром? (если нас будет много, то волонтёрить придётся не больше раза в год!!!', reply_markup=make_keyboard_column(yes_no_buttons))
    await state.set_state(UserRegistration.choosing_autovolonteur)

@router.message(UserRegistration.choosing_autovolonteur, Text(text=yes_no_buttons))
async def choosed_autovolonteur(message: Message, state: FSMContext):
    await state.update_data(autovolonteur=message.text)
    state_data = await state.get_data()
    if state_data['status'] == available_statuses[0]:
        await message.answer('Спасибо. Регистрация завершена')
        await state.clear()
    else:
        await message.answer(text='Есть ли у вас водительские права?', reply_markup=make_keyboard_column(yes_no_buttons))
        await state.set_state()

@router.message(UserRegistration.choosing_having_rights, Text(text=yes_no_buttons))
async def choosed_having_rights(message: Message, state: FSMContext):
    pass