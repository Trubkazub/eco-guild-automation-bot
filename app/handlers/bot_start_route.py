from distutils.util import strtobool

from email_validator import validate_email, EmailNotValidError

from app.handlers.custom_validators import VK_link_validator, VkLinkException

from typing import Optional

from aiogram.utils.markdown import hlink
from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.message import Message
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

from app.bot_main import bot
from app.handlers.filters import ContactFilter
from app.keyboards.inline_keyboard_functions import make_inline_keyboard, yes_no_inline_keyboard
from app.keyboards.keyboard_functions import phone_request_keyboard

router = Router()
available_statuses = ['Учащийся в школе', 'Студент/Аспирант', 'Выпускник']
available_vuzes = ['МГУ', 'Другой']
available_fakultets = ['Биологический факультет', 'Биотехнологический факультет', 'Высшая школа бизнеса',
                       'Высшая школа государственного администрирования', 'Высшая школа государственного аудита',
                       'Высшая школа инновационного бизнеса',
                       'Высшая школа культурной политики и управления в гуманитарной сфере', 'Высшая школа перевода',
                       'Высшая школа современных социальных наук', 'Высшая школа телевидения',
                       'Высшая школа управления и инноваций', 'Географический факультет', 'Геологический факультет',
                       'Институт стран Азии и Африки', 'Исторический факультет', 'Механико–математический факультет',
                       'Московская школа экономики', 'Социологический факультет',
                       'Факультет биоинженерии и биоинформатики', 'Факультет вычислительной математики и кибернетики',
                       'Факультет глобальных процессов', 'Факультет государственного управления',
                       'Факультет журналистики', 'Факультет иностранных языков и регионоведения', 'Факультет искусств',
                       'Факультет космических исследований', 'Факультет мировой политики',
                       'Факультет наук о материалах', 'Факультет педагогического образования', 'Факультет политологии',
                       'Факультет почвоведения', 'Факультет психологии', 'Факультет фундаментальной медицины',
                       'Факультет фундаментальной физико-химической инженерии', 'Физический факультет',
                       'Филологический факультет', 'Философский факультет', 'Химический факультет',
                       'Экономический факультет', 'Юридический факультет']
available_years = ['I курс бакалавриата', 'II курс бакалавриата', 'III курс бакалавриата', 'IV курс бакалавриата',
                   'I курс магистратуры', 'II курс магистратуры', 'I курс специалитета', 'II курс специалитета',
                   'III курс специалитета', 'IV курс специалитета', 'V курс специалитета', 'VI курс специалитета',
                   'I курс аспирантуры', 'II курс аспирантуры', 'III курс аспирантуры', 'IV курс аспирантуры']

degree_stages = ['Бакалавриата', 'Магистратура', 'Специалитет', 'Аспирантура', 'Докторантура']


class UserRegistration(StatesGroup):
    entering_name = State()
    entering_surname = State()
    entering_middlename = State()
    choosing_status = State()
    entering_school = State()
    entering_class = State()
    choosing_vuz = State()
    entering_vuz = State()
    choosing_fakultet = State()
    entering_fakultet = State()
    choosing_year = State()
    choosing_max_grade = State()
    choosing_science_degree = State()
    entering_science_degree = State()
    entering_phone = State()
    entering_email = State()
    entering_vk = State()
    choosing_autovolonteur = State()
    choosing_having_rights = State()
    choosing_having_car = State()
    choosing_using_carsharing = State()
    accept_confidential = State()
    finished = State()


class Step:
    callback_query: Optional[CallbackQuery]
    message: Optional[Message]
    state: FSMContext
    next_state: Optional[State]
    chosen_answer: Optional[str]
    next_message: str
    reply_markup: Optional[ReplyKeyboardMarkup | InlineKeyboardMarkup | ReplyKeyboardRemove]
    data: Optional[dict]
    parse_mode: Optional[str]

    def __init__(self, **kwargs):
        self.callback_query = kwargs.get('callback_query')
        self.message = kwargs.get('message')
        self.state = kwargs.get('state')
        self.next_state = kwargs.get('next_state')
        self.chosen_answer = kwargs.get('chosen_answer')
        self.next_message = kwargs.get('next_message')
        self.reply_markup = kwargs.get('reply_markup')
        self.parse_mode = kwargs.get('parse_mode')
        self.data = kwargs.get('data')

    async def process_step(self):
        if self.callback_query:
            await bot.answer_callback_query(self.callback_query.id)
            if self.chosen_answer:
                await self.callback_query.message.edit_reply_markup()
                await self.callback_query.message.edit_text(f'{self.callback_query.message.html_text}\n\n— '
                                                            f'{self.chosen_answer}', parse_mode='HTML')
            self.message = self.callback_query.message
        if self.data:
            await self.state.update_data(**self.data)
        await self.message.answer(text=self.next_message, reply_markup=self.reply_markup, parse_mode=self.parse_mode)
        if self.next_state:
            await self.state.set_state(self.next_state)


def bool_to_str(b: int) -> str:
    if b:
        return 'Да'
    else:
        return 'Нет'


@router.message(Command(commands=['start']))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer('Привет! Рады приветствовать тебя в ЭкоГильдии!')
    await message.answer('Напиши, пожалуйста информацию о себе, которая понадобится нам для создания именных '
                         'благодарственных писем, котируемых при подаче на ПГАС!')
    data = {'username': message.from_user.username, "user_id": message.from_user.id, "chat_id": message.chat.id}
    step = Step(message=message, state=state, next_state=UserRegistration.entering_surname, next_message='Фамилия',
                data=data,
                reply_markup=ReplyKeyboardRemove())
    await step.process_step()


@router.message(UserRegistration.entering_name)
async def name_entered(message: Message, state: FSMContext):
    step = Step(message=message, state=state, data={"name": message.text.lower()}, next_message='Отчество',
                next_state=UserRegistration.entering_middlename)
    await step.process_step()


@router.message(UserRegistration.entering_surname)
async def surname_entered(message: Message, state: FSMContext):
    step = Step(message=message, state=state, data={"surname": message.text.lower()}, next_message='Имя',
                next_state=UserRegistration.entering_name)
    await step.process_step()


@router.message(UserRegistration.entering_middlename)
async def middlename_entered(message: Message, state: FSMContext):
    step = Step(message=message, state=state, data={"middlname": message.text.lower()}, next_message='Статус',
                next_state=UserRegistration.choosing_status, reply_markup=make_inline_keyboard(available_statuses))
    await step.process_step()


@router.callback_query(UserRegistration.choosing_status)
async def choosed_status(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == '0':
        step = Step(callback_query=callback_query, state=state,
                    data={"status": available_statuses[int(callback_query.data)].lower()},
                    next_message='Название школы',
                    next_state=UserRegistration.entering_school,
                    chosen_answer=available_statuses[int(callback_query.data)])
    else:
        step = Step(callback_query=callback_query, state=state,
                    data={"status": available_statuses[int(callback_query.data)].lower()}, next_message='ВУЗ',
                    next_state=UserRegistration.choosing_vuz,
                    chosen_answer=available_statuses[int(callback_query.data)],
                    reply_markup=make_inline_keyboard(available_vuzes))
    await step.process_step()


@router.message(UserRegistration.entering_school)
async def entered_school(message: Message, state: FSMContext):
    step = Step(message=message, state=state, data={"school": message.text.lower()}, next_message='Класс обучения',
                next_state=UserRegistration.entering_class)
    await step.process_step()


@router.message(UserRegistration.entering_class)
async def entered_class(message: Message, state: FSMContext):
    step = Step(message=message, state=state, data={"clas": message.text.lower()},
                next_message='Телефон (используем его крайне редко, но иногда всё же важна возможность оперативной '
                             'связи с волонтёром):',
                next_state=UserRegistration.entering_phone, reply_markup=phone_request_keyboard())
    await step.process_step()


@router.callback_query(UserRegistration.choosing_vuz)
async def choosed_vuz(callback_query: CallbackQuery, state: FSMContext):
    data = {'vuz': available_vuzes[int(callback_query.data)].lower()}
    if callback_query.data == '0':
        step = Step(callback_query=callback_query, state=state,
                    data=data, chosen_answer=available_vuzes[int(callback_query.data)], next_message='Факультет',
                    reply_markup=make_inline_keyboard(available_fakultets),
                    next_state=UserRegistration.choosing_fakultet)
    else:
        step = Step(callback_query=callback_query, state=state,
                    data=data, chosen_answer=available_vuzes[int(callback_query.data)], next_message='Какой именно?',
                    next_state=UserRegistration.entering_vuz)
    await step.process_step()


@router.message(UserRegistration.entering_vuz)
async def entered_vuz(message: Message, state: FSMContext):
    step = Step(message=message, state=state, data={'vuz': message.text}, next_message='Факультет',
                next_state=UserRegistration.entering_fakultet)
    await step.process_step()


@router.message(UserRegistration.entering_fakultet)
async def entered_fakultet(message: Message, state: FSMContext):
    data = {'fakultet': message.text.lower()}
    state_data = await state.get_data()
    if state_data['status'] == available_statuses[2].lower():
        step = Step(message=message, state=state, data=data,
                    next_message='Максимально полученная ступень высшего образования:',
                    reply_markup=make_inline_keyboard(degree_stages), next_state=UserRegistration.choosing_max_grade)
    else:
        step = Step(message=message, state=state, data=data,
                    next_message='Статус:', reply_markup=make_inline_keyboard(available_years),
                    next_state=UserRegistration.choosing_year)
    await step.process_step()


@router.callback_query(UserRegistration.choosing_fakultet)
async def choosed_fakultet(callback_query: CallbackQuery, state: FSMContext):
    data = {'fakultet': available_fakultets[int(callback_query.data)].lower()}
    state_data = await state.get_data()
    if state_data['status'] == available_statuses[2].lower():
        step = Step(callback_query=callback_query, state=state, data=data,
                    chosen_answer=available_fakultets[int(callback_query.data)],
                    next_message='Максимально полученная ступень высшего образования:',
                    reply_markup=make_inline_keyboard(degree_stages), next_state=UserRegistration.choosing_max_grade)
    else:
        step = Step(callback_query=callback_query, state=state, data=data,
                    chosen_answer=available_fakultets[int(callback_query.data)],
                    next_message='Статус:', reply_markup=make_inline_keyboard(available_years),
                    next_state=UserRegistration.choosing_year)
    await step.process_step()


@router.callback_query(UserRegistration.choosing_max_grade)
async def choosed_max_degree(callback_query: CallbackQuery, state: FSMContext):
    stage = degree_stages[int(callback_query.data)]
    data = {'max_degree': stage.lower()}
    if degree_stages.index(stage) >= 3:
        step = Step(callback_query=callback_query, state=state, chosen_answer=stage, data=data,
                    next_message='Есть научная степень?', reply_markup=yes_no_inline_keyboard(),
                    next_state=UserRegistration.choosing_science_degree)
    else:
        step = Step(callback_query=callback_query, state=state, chosen_answer=stage, data=data,
                    next_message='Телефон (используем его крайне редко, но иногда всё же важна возможность '
                                 'оперативной связи с волонтёром):', reply_markup=phone_request_keyboard(),
                    next_state=UserRegistration.choosing_science_degree)
    await step.process_step()


@router.callback_query(UserRegistration.choosing_science_degree)
async def choosed_science_degree(callback_query: CallbackQuery, state: FSMContext):
    science_degree = strtobool(callback_query.data)
    if science_degree:
        step = Step(callback_query=callback_query, state=state, chosen_answer=bool_to_str(science_degree),
                    next_message='Укажите, пожалуйста, вашу научную степень',
                    next_state=UserRegistration.entering_science_degree)
    else:
        step = Step(callback_query=callback_query, state=state, chosen_answer=bool_to_str(science_degree),
                    next_state=UserRegistration.entering_phone, reply_markup=phone_request_keyboard(),
                    next_message='Телефон (используем его крайне редко, но иногда всё же важна возможность '
                                 'оперативной связи с волонтёром): ')
    await step.process_step()


@router.message(UserRegistration.entering_science_degree)
async def entered_science_degree(message: Message, state: FSMContext):
    step = Step(message=message, state=state, data={'science_degree': message.text.lower()},
                reply_markup=phone_request_keyboard(), next_state=UserRegistration.entering_phone,
                next_message='Телефон (используем его крайне редко, но иногда всё же важна возможность '
                             'оперативной связи с волонтёром): ')
    await step.process_step()


@router.callback_query(UserRegistration.choosing_year)
async def choosed_year(callback_query: CallbackQuery, state: FSMContext):
    year = available_years[int(callback_query.data)]
    step = Step(callback_query=callback_query, state=state, data={'year': year.lower()}, chosen_answer=year,
                next_state=UserRegistration.entering_phone, reply_markup=phone_request_keyboard(),
                next_message='Телефон (используем его крайне редко, но иногда всё же важна возможность '
                             'оперативной связи с волонтёром): ')
    await step.process_step()


@router.message(UserRegistration.entering_phone, ContactFilter())
async def entered_phone(message: Message, state: FSMContext):
    step = Step(message=message, state=state, data={'phone_number': message.contact.phone_number},
                reply_markup=ReplyKeyboardRemove(), next_state=UserRegistration.entering_email,
                next_message='Введите электронную почту')
    await step.process_step()


@router.message(UserRegistration.entering_phone, Text(text='Пропустить'))
async def skipped_phone(message: Message, state: FSMContext):
    step = Step(message=message, state=state, reply_markup=ReplyKeyboardRemove(),
                next_state=UserRegistration.entering_email,
                next_message='Введите электронную почту')
    await step.process_step()


@router.message(UserRegistration.entering_phone)
async def wrong_phone_answer(message: Message, state: FSMContext):
    await message.answer('Пожалуйста, выберите вариант из списка ниже', reply_markup=phone_request_keyboard())


@router.message(UserRegistration.entering_email)
async def entered_phone(message: Message, state: FSMContext):
    email = message.text
    try:
        validation = validate_email(email, check_deliverability=True)
    except EmailNotValidError:
        await message.answer('Пожалуйста, введите корректный e-mail')
    else:
        step = Step(message=message, state=state, data={'email': validation.email},
                    next_state=UserRegistration.entering_vk,
                    next_message='Введите ссылку на профиль ВК')
        await step.process_step()


@router.message(UserRegistration.entering_vk)
async def entered_phone(message: Message, state: FSMContext):
    vk = VK_link_validator(message.text)
    try:
        vk.validate_url()
    except VkLinkException:
        await message.answer('Пожалуйста, ведите корректную ссылку на профиль ВК, начинающуюся с https://vk.com/')
    else:
        vk = vk.url
        state_data = await state.get_data()
        if state_data['status'] == available_statuses[0].lower():
            step = Step(message=message, state=state, data={'vk': vk}, parse_mode='HTML',
                        reply_markup=make_inline_keyboard(['Да']), next_state=UserRegistration.accept_confidential,
                        next_message='Согласиться с нашей '
                                     + hlink('политикой конфиденциальности',
                                             'https://docs.google.com/document/d/1zcfX5KnB97az41Sq4NeioCwp'
                                             '-XAH5SC1oOjdxSwNRaA/edit') + '?')
        else:
            step = Step(message=message, state=state, data={'vk': vk}, reply_markup=make_inline_keyboard(['Хорошо']),
                        next_state=UserRegistration.choosing_autovolonteur,
                        next_message='Далее пойдут вопросы о том, можете ли вы стать потенциальным автоволонтёром (если '
                                     'наберётся достаточно человек, волонтёрить придётся не больше раза в год!) Затраты на '
                                     'бензин или каршеринг мы возмещаем')
        await step.process_step()


@router.callback_query(UserRegistration.choosing_autovolonteur)
async def choosed_autovolonteur(callback_query: CallbackQuery, state: FSMContext):
    step = Step(callback_query=callback_query, state=state, reply_markup=yes_no_inline_keyboard(),
                next_state=UserRegistration.choosing_having_rights, chosen_answer='Хорошо',
                next_message='Есть права? Достаточно стандартных прав на легковую машину, категории B')
    await step.process_step()


@router.callback_query(UserRegistration.choosing_having_rights)
async def choosed_having_rights(callback_query: CallbackQuery, state: FSMContext):
    having_rights = strtobool(callback_query.data)
    if having_rights:
        step = Step(callback_query=callback_query, state=state, data={'having_rights': having_rights},
                    chosen_answer=bool_to_str(having_rights), reply_markup=yes_no_inline_keyboard(),
                    next_state=UserRegistration.choosing_having_car, next_message='Есть своя машина?')
    else:
        step = Step(callback_query=callback_query, state=state, data={'having_rights': having_rights},
                    chosen_answer=bool_to_str(having_rights), reply_markup=make_inline_keyboard(['Да']),
                    parse_mode='HTML', next_state=UserRegistration.accept_confidential,
                    next_message='Согласиться с нашей '
                                 + hlink('политикой конфиденциальности',
                                         'https://docs.google.com/document/d/1zcfX5KnB97az41Sq4NeioCwp-XAH5SC1oOjdxSwNRaA/edit')
                                 + '?')
    await step.process_step()


@router.callback_query(UserRegistration.choosing_having_car)
async def choosed_having_car(callback_query: CallbackQuery, state: FSMContext):
    having_car = strtobool(callback_query.data)
    step = Step(callback_query=callback_query, state=state, data={'having_car': having_car},
                chosen_answer=bool_to_str(having_car), reply_markup=yes_no_inline_keyboard(),
                next_state=UserRegistration.choosing_using_carsharing,
                next_message='Можете ли вы быть автоволонтёром на каршеринге?')
    await step.process_step()


@router.callback_query(UserRegistration.choosing_using_carsharing)
async def choosed_using_carsharing(callback_query: CallbackQuery, state: FSMContext):
    using_carsharing = strtobool(callback_query.data)
    step = Step(callback_query=callback_query, state=state, data={'using_carsharing': using_carsharing},
                chosen_answer=bool_to_str(using_carsharing), parse_mode='HTML',
                reply_markup=make_inline_keyboard(['Да']), next_state=UserRegistration.accept_confidential,
                next_message='Согласиться с нашей ' +
                             hlink('политикой конфиденциальности',
                                   'https://docs.google.com/document/d/1zcfX5KnB97az41Sq4NeioCwp-XAH5SC1oOjdxSwNRaA'
                                   '/edit') + '?')
    await step.process_step()


@router.callback_query(UserRegistration.accept_confidential)
async def accepted_confidentional(callback_query: CallbackQuery, state: FSMContext):
    step = Step(callback_query=callback_query, state=state, chosen_answer='Да',
                reply_markup=make_inline_keyboard(['Отлично']), next_state=UserRegistration.finished,
                next_message='Благодарим вас за уделённое время! Профиль был успешно зарегистрирован!')
    await step.process_step()


@router.callback_query(UserRegistration.finished)
async def finished(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup()
    await callback_query.message.edit_text('Благодарим вас за уделённое время! Профиль был успешно '
                                           'зарегистрирован!\n\n— Отлично!')
    await state.clear()
