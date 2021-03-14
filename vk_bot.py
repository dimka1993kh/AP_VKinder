import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from bs4 import BeautifulSoup
from functions import create_text_keyboard, add_next_button, age_verification, checking_number_in_str, get_user_sex, checking_city_entries, find_russia_cities, find_citi_in_VK, convert_data_for_message, opposite_sex, analize_color_button
from classes import VKUser
from pprint import pprint
from data import empty_keyboard
import json
from db.main import Base, engine, Session
from db.models import Vkinder_result
from sqlalchemy.sql.expression import func

class VkBot:
    
    def __init__(self, user_id):
        print("Создан объект бота!")
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)
        self._USER_SEX = get_user_sex(self._USER_ID)
        self.answers = {'marital_status' : [], 'correction' : False}
        self.count = 0
        self.function_variable = []
        self.keyboard = VkKeyboard.get_empty_keyboard()
        self.marital_status_male = ['НЕ ЖЕНАТ', 'ВСТРЕЧАЮСЬ', 'ПОМОЛВЛЕН', 'ЖЕНАТ', 'В ГРАЖДАНСОКМ БРАКE', 'ВЛЮБЛЕН', 'ВСЕ СЛОЖНО', 'В АКТИВНОМ ПОИСКЕ']
        self.marital_status_female = ['НЕ ЗАМУЖЕМ', 'ВСТРЕЧАЮСЬ', 'ПОМОЛВЛЕНА', 'ЗАМУЖЕМ', 'В ГРАЖДАНСОКМ БРАКE', 'ВЛЮБЛЕНА', 'ВСЕ СЛОЖНО', 'В АКТИВНОМ ПОИСКЕ']
        self.result = {'response': {'count': 0, 'items' : []}}
        self.person_photos = ''
        self.person_count = 0
        self.removable_urls = []
        # Порядковый номер вопроса. Изменяется, когда пользователь ответил на вопрос. Используется для определения следующего вопроса
        self.control_questions = 0
    
    # Метод, возвращающий username по id
    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id"+str(user_id))
        bs = BeautifulSoup(request.text, "html.parser")
        
        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])
        
        return user_name.split()[0]
    
    # Метод, возвращающий все параметры в изначальное состояние для нового поиска
    def return_standard_values(self):
        self.answers = {'marital_status' : [], 'correction' : False}
        self.person_count = 0
        self.person_photos = ''
        self.result = {'response': {'count': 0, 'items' : []}}
        self.count = 0
        self.function_variable = 0
        
    # Метод для очистки от ненужных тэгов
    @staticmethod
    def _clean_all_tag_from_str(string_line):
        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """
        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True
        
        return result
    # Метод, позволяющий сделать записть ответа пользователя
    def write_answer(self, message, question_name):
        if question_name in self.answers.keys() and isinstance(self.answers[question_name], list):
            self.answers[question_name].append(message)
        else:
            self.answers[question_name] = message
    # Метод, который был нужен для отладки. Просто печатает в консоль ответы пользователя
    def print_answers(self):
        print('Ответы', self.answers)
    # Метод, который переводит семейное положение из человеческого вида в соответсвующее цифровое обозначение
    def convert_status(self):
        result = []
        for el in self.answers['marital_status']:
            if el == 'НЕ ЖЕНАТ' or el == 'НЕ ЗАМУЖЕМ':
                result.append('1')
            elif el == 'ВСТРЕЧАЕТСЯ':
                result.append('2')
            elif el == 'ПОМОЛВЛЕН' or el == 'ПОМОЛВЛЕНА':
                result.append('3')
            elif el == 'ЖЕНАТ' or el == 'ЗАМУЖЕМ':
                result.append('4')
            elif el == 'ВСЕ СЛОЖНО':
                result.append('5')
            elif el == 'В АКТИВНОМ ПОИСКЕ':
                result.append('6')
            elif el == 'ВЛЮБЛЕН' or el == 'ВЛЮБЛЕНА':
                result.append('7')
            elif el == 'В ГРАЖДАНСКОМ БРАКЕ':
                result.append('8')
        return result
    # Метод, который осуществляет поиск пар
    def search_people(self, search_dict:dict=None):
        if not search_dict:
            search_dict = {
                'sex' : self.answers['sex'],
                'status' : self.convert_status(),
                'age_from' : self.answers['min_age'],
                'age_to' : self.answers['max_age'],
                'city' : self.answers['city']['id']
            }
        # Поиск по друзьям друзей
        # result = VKUser(self._USER_ID, search_dict).search_pepople()
        # Поиск по всему ВК
        result = VKUser(self._USER_ID, search_dict).search_people_by_users_search(self.removable_urls)
        return result
    # Метод возвращения исключения
    def new_message_exception(self):
        return f"Я бот.Я не понял твоего ответа. Пожалуйста, ответь на вопрос."
    # Метод создания клавиатуры
    def create_keyboard(self, buttons_list:list=None):
        keyboard = VkKeyboard(one_time=True)
        num_button_in_line = 0
        if buttons_list:
            for button in buttons_list:
                if button[1] in ['POSITIVE', 'NEGATIVE', 'PRIMARY', 'SECONDARY']:
                    if num_button_in_line == 2:
                        keyboard.add_line()
                        num_button_in_line = 0
                    color = analize_color_button(button[1])
                    keyboard.add_button(f'{button[0]}', color=color)
                    num_button_in_line += 1
                else:
                    raise Exception(f'Неверно введен цвет кнопки при создании клавиатуры в вопросе {self.control_questions}')
            keyboard = keyboard.get_keyboard()
        else:
            keyboard = VkKeyboard.get_empty_keyboard()
        
        # Запишем клавиатуру в переменную на случай, если нам нужно будет ее снова показать
        self.keyboard = keyboard

        return keyboard
    # Метод, показывающий пары пользователю
    def show_matched_pair(self, message):
        # Создадим клавиатуру
        # Если пара последняя в поиске
        if self.person_count == self.result['response']['count'] - 1:
            keyboard = self.create_keyboard([['Посмотреть следующие 10 вариантов', 'POSITIVE'], ['Начать поиск заново', 'NEGATIVE']])
        else:
            keyboard = self.create_keyboard([['Далее', 'POSITIVE']])

        data = convert_data_for_message(self, self.control_questions - 99)
        bot_answer = data['bot_answer']
        person_photos = data['person_photos']

        # Определимся со следующим сообщением на основании ответа
        self.write_answer(message.upper(), f'person_{self.control_questions - 99}')
        self.control_questions += 1
        self.person_count += 1

        return {'bot_answer' : bot_answer, 'person_photos' : person_photos, 'keyboard' : keyboard}
    # Метод получения пользователей, которых мы будем исключать из повторного поиска
    def get_removable_urls(self):
        for person in self.result['response']['items']:
            self.removable_urls.append(person['src'])   
    # Метод записи результата в базу данных PostgreSql
    def write_to_bd(self):
        # Инициализируем схему
        Base.metadata.create_all(engine)
        # Начнем сессию
        session = Session()
        # Определим индекс последнего элемента в db
        max_id_in_db = session.query(func.max(Vkinder_result.id)).first()[0]
        if max_id_in_db:
            max_id = max_id_in_db
        else:
            max_id = 0
        # Разберемся с фотографиями, так как не у всех есть 3 фотографии в профиле
        for idx, person in enumerate(self.result['response']['items']):
            photos = ['', '', '']
            for photo_idx, photo_src in enumerate(person['top_photo']):
                photos[photo_idx] = photo_src['src']
            # Запишем результат в таблицу
            result = Vkinder_result(id=max_id + idx + 1, first_name=person['first_name'], last_name=person['last_name'], link=person['src'], photo_1=photos[0], photo_2=photos[1], photo_3=photos[2])
            session.add(result)
        session.commit()

        # yesterday = db.session.query(db.func.max(Setting.count)).first()[0]

    # Метод, позволяющий написать пользователя сообщение
    def new_message(self, message):
        
        print('message', message)


        # Получение ответов пользователя для отладки
        if message == '!':
            self.print_answers()
            bot_answer = f'Написал твои ответы. Это нужно только для отладки :).'
            keyboard = VkKeyboard.get_empty_keyboard()

        elif message.upper() == 'НАЧАТЬ':
            # Создадим клавиатуру
            # keyboard = self.create_keyboard([['Да', 'POSITIVE'], ['Нет, NEGATIVE']])
            keyboard = self.create_keyboard([['Да', 'POSITIVE'], ['Нет', 'NEGATIVE']])
            # keyboard.add_button('Да', color=VkKeyboardColor.POSITIVE)
            # keyboard.add_button('Нет', color=VkKeyboardColor.NEGATIVE)
            # keyboard = keyboard.get_keyboard()

            # Определимся со следующим сообщением на основании ответа
            self.control_questions = 1

            # Зададим вопрос
            bot_answer = f"Привет, {self._USERNAME}! Я чат-бот сообщества 'VKinder'. Помогу тебе найти себе пару.\n Хочешь уточнить параметры поиска?"

        elif self.control_questions == 0:
            if message.upper() != 'НАЧАТЬ':
                # Создадим клавиатуру
                keyboard = self.create_keyboard()

                # Отреагируем на ответ пользователя
                bot_answer = self.new_message_exception()
            
        # Если пользователь начал общение с ботом
        elif self.control_questions == 1:
            # Определение следующего вопроса
            if message.upper() == 'НЕТ':
                # Создадим клавиатуру
                keyboard = self.create_keyboard()
                # Определимся со следующим сообщением на основании ответа
                self.control_questions = 2
                self.write_answer(False, 'correction')
                # Зададим вопрос
                bot_answer = f'Напиши, сколько тебе лет?'
            elif message.upper() == 'ДА':
                # Создадим клавиатуру
                keyboard = self.create_keyboard([['Мужчину', 'POSITIVE'], ['Девушку', 'POSITIVE']])

                # Определимся со следующим сообщением на основании ответа
                self.control_questions = 3
                self.write_answer(True, 'correction')

                # Зададим вопрос
                bot_answer = f"Хорошо. Тогда ответь на вопрос, ты ищешь мужчину или девушку?"

            # В случае, если пользователь вводит неожиданный вариант
            else:
                # Создадим клавиатуру
                keyboard = self.keyboard
                # Вопрос остается тем же
                # Отреагируем на ответ пользователя
                bot_answer = self.new_message_exception()

        # Если пользователь не согласен дать уточнения на поиск, то он должен ответить на вопрос, сколько тебе лет?
        elif self.control_questions == 2: 
            # Проверяем на число
            if message.isdigit():
                # Зададим параметры для поиска
                self.answers = {'marital_status' : ['6'],
                                'age' : message,
                                'sex' : opposite_sex(self._USER_SEX),
                                'min_age': int(message) - 3,
                                'max_age': int(message) + 3,
                                'city' : VKUser(self._USER_ID).find_city(),
                                'correction' : True,
                                }

                # Начнем поиск людей
                # Функция search_people ищет пользователей по всему ВК
                self.result = self.search_people()
                self.write_to_bd()

                # Создадим клавиатуру
                keyboard = self.create_keyboard([['Да', 'POSITIVE'], ['Начать сначала', 'NEGATIVE']])

                # Определимся со следующим сообщением на основании ответа
                self.control_questions = 100

                # Зададим вопрос
                bot_answer = f"Нашли тебе {self.result['response']['count']} вариантов. Начнем смотреть?"
            # Если пользователь ввел не число или отрицательное число
            else:
                # Создадим клавиатуру
                keyboard = self.keyboard
                # Вопрос остается тем же
                # Отреагируем на ответ пользователя
                bot_answer = self.new_message_exception()

        # Если пользователь согласился уточнить поиск, он отвечает на вопрос, мужчину или девушку?
        elif self.control_questions == 3:
            if message.upper() in ['МУЖЧИНУ', 'ДЕВУШКУ']:
                if message.upper() == 'МУЖЧИНУ':
                    self.write_answer('2', 'sex')
                elif message.upper() == 'ДЕВУШКУ':
                    self.write_answer('1', 'sex')
                
                # Создадим клавиатуру
                    keyboard = self.create_keyboard()
                
                # Определимся со следующим сообщением на основании ответа
                    self.control_questions = 4

                # Зададим вопрос
                bot_answer = f"Сколько минимум лет должно быть товей половинке?"
            else:
                # Создадим клавиатуру
                keyboard = self.keyboard
                # Вопрос остается тем же
                # Отреагируем на ответ пользователя
                bot_answer = self.new_message_exception()
        # Пользователь должен ввести минимальный возраст
        elif self.control_questions == 4:
            if message.isdigit():

                # Создадим клавиатуру
                keyboard = self.create_keyboard()

                if age_verification({'min_age': int(message)}):

                    # Определимся со следующим сообщением на основании ответа
                    self.control_questions = 5
                    self.write_answer(int(message), 'min_age')

                    # Зададим вопрос
                    bot_answer = f"Сколько минимум лет должно быть товей половинке? Возраст должен быть не меньше {self.answers['min_age']}."

                else:
                    # Отреагируем на ответ пользователя
                    bot_answer = f"Минимальный возраст введен не верно. Должен быть положительный. Введи верный возраст."

            else:
                # Создадим клавиатуру
                keyboard = self.keyboard
                # Вопрос остается тем же
                # Отреагируем на ответ пользователя
                bot_answer = self.new_message_exception()
        elif self.control_questions == 5:
            if message.isdigit():
                # Создадим клавиатуру
                keyboard = self.create_keyboard()

                if age_verification({'max_age': int(message)}, int(self.answers['min_age'])):

                    # Определимся со следующим сообщением на основании ответа
                    self.control_questions = 6
                    self.write_answer(int(message), 'max_age')

                    # Зададим вопрос
                    bot_answer = f"В каком городе планируешь искать?"

                else:

                    # Отреагируем на ответ пользователя
                    bot_answer = f"Максимальный возраст должен быть больше {self.answers['min_age']}. Введи верный возраст."

            else:
                print(4)
                # Создадим клавиатуру
                keyboard = self.keyboard
                # Вопрос остается тем же
                # Отреагируем на ответ пользователя
                bot_answer = self.new_message_exception()

        elif self.control_questions == 6:

            # Пробуем найти город
            citi_list = find_citi_in_VK(self._USER_ID, message.upper())

            # Если при проверке города в ВК имеется несколько таких городов, то просим пользователя уточнить наименование города
            if len(citi_list) > 1 and self.count == 0:
                bot_answer = f"Найдено несколько мест:"
                for idx, city in enumerate(citi_list):
                        self.function_variable.append(idx + 1)
                        bot_answer += f"\n{idx + 1} - "
                        for field in list(city.keys()):
                            if field != 'id':
                                bot_answer += f"{city[field]}, "
                        bot_answer += '\nВыбери нужный город.'

                # Создадим клавиатуру
                colors = []
                for city in self.function_variable:
                    colors.append('POSITIVE')
                keyboard = self.create_keyboard(zip(self.function_variable, colors))

                self.write_answer(citi_list, 'city') 

                # Используем count для того, чтобы при нажатии на кнопку города в if программа не начала искать город по номеру кнопки
                self.count = 1

            elif not citi_list:
                # Отреагируем на ответ пользовател
                bot_answer = 'Такой город не найден. Проверь вводимые данные'

                # Создадим клавиатуру
                keyboard = self.create_keyboard()
            
            else:
                # Создадим клавиатуру
                colors = []
                for status in self.marital_status_male:
                    colors.append('POSITIVE')
                if self.answers['sex'] == 'male':
                    keyboard = self.create_keyboard(zip(self.marital_status_male, colors))
                else:
                    keyboard = self.create_keyboard(zip(self.marital_status_female, colors))

                # Зададим вопрос
                bot_answer = f"В каком семейном положении находится человек?"

                # Определимся со следующим сообщением на основании ответа
                self.control_questions = 7

                if self.count == 0:
                    self.write_answer(citi_list[0], 'city')
                elif int(message) in self.function_variable:
                    self.answers['city'] = self.answers['city'][int(message) - 1]
                else:
                    # Создадим клавиатуру
                    keyboard = self.keyboard
                    # Вопрос остается тем же
                    # Отреагируем на ответ пользователя
                    bot_answer = self.new_message_exception()

        elif self.control_questions == 7:
            if message.upper() in self.marital_status_male or message.upper() in self.marital_status_female:
                print(1)

                # Создадим клавиатуру
                keyboard = self.create_keyboard([['Да', 'POSITIVE'], ['НАЧАТЬ ПОИСК ЗАНОВО', 'NEGATIVE']])

                # Определимся со следующим сообщением на основании ответа
                self.control_questions = 100
                self.write_answer(message.upper(), 'marital_status')

                # Начнем поиск людей
                # Функция search_people ищет пользователей по всему ВК
                self.result = self.search_people()
                self.write_to_bd()


                # Зададим вопрос
                bot_answer = f"Нашли тебе {self.result['response']['count']} вариантов. Начнем смотреть?"

            else:
                print(2)
                # Создадим клавиатуру
                keyboard = self.keyboard
                # Вопрос остается тем же
                # Отреагируем на ответ пользователя
                bot_answer = self.new_message_exception()

        # Покажем пользователю количество пар, не превышающее self.result['response']['count']
        elif self.person_count < self.result['response']['count']:
            if self.control_questions >= 100:
                data = self.show_matched_pair(message)
                bot_answer = data['bot_answer']
                self.person_photos = data['person_photos']
                keyboard = data['keyboard']

        elif message.upper() == 'ПОСМОТРЕТЬ СЛЕДУЮЩИЕ 10 ВАРИАНТОВ':
            # Находим url предыдущих пользователей
            self.get_removable_urls()
            self.person_photos = ''
            self.person_count = 0
            self.control_questions = 100
            # Создадим клавиатуру
            keyboard = self.create_keyboard([['Да', 'POSITIVE'], ['НАЧАТЬ ПОИСК ЗАНОВО', 'NEGATIVE']])

            # Определимся со следующим сообщением на основании ответа
            self.control_questions = 100

            # Начнем поиск людей
            # Функция search_people ищет пользователей по всему ВК
            self.result = self.search_people()
            self.write_to_bd()

            # Зададим вопрос
            bot_answer = f"Нашли тебе еще {self.result['response']['count']} вариантов. Начнем смотреть?"

        # Если пользователю никто не понравился, то начинаем поиск заново
        elif message.upper() == 'НАЧАТЬ ПОИСК ЗАНОВО':

            # Создадим клавиатуру
            keyboard = self.create_keyboard([['Начать', 'SECONDARY']])

            # Определимся со следующим сообщением на основании ответа
            self.control_questions = 0
            # Отреагируем на ответ пользователя
            bot_answer = f'Очень жаль, что тебе никто не понравился. Давай попробуем сначала:)'

            # Восстановим все по-умолчанию
            self.return_standard_values()






            # Покажем пользователю количество пар, не превышающее self.result['response']['count']
        
        return {'message' : bot_answer, 'keyboard' : keyboard, 'mediafile' : self.person_photos}