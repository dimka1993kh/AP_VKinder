import requests
from bs4 import BeautifulSoup
from functions import create_text_keyboard, add_next_button, age_verification, checking_number_in_str, get_user_sex, checking_city_entries, find_russia_cities, find_citi_in_VK, convert_data_for_message, opposite_sex
from classes import VKUser
from pprint import pprint

class VkBot:
    
    def __init__(self, user_id):
        print("Создан объект бота!")
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)
        self._USER_SEX = get_user_sex(self._USER_ID)
        self.control_field_occupancy = {
                                        'start' : False,
                                        'age' : False,
                                        'correction' : False,
                                        'sex' : False,
                                        'min_age' : False,
                                        'max_age' : False,
                                        'city' : False,
                                        'marital_status' : False,
                                        'person_1' : False,
                                        'person_2' : False,
                                        'person_3' : False,
                                        'person_4' : False,
                                        'person_5' : False,
                                        'person_6' : False,
                                        'person_7' : False,
                                        'person_8' : False,
                                        'person_9' : False,
                                        'person_10' : False,
                                        }
        self.answers = {'marital_status' : [], 'correction' : False}
        self.count = 0
        self.function_variable = 0
        self.keyboard = {
                            "one_time":False,
                            "buttons":[],
                            "inline" : False
                        }
        self.marital_status_male = ['НЕ ЖЕНАТ', 'ВСТРЕЧАЮСЬ', 'ПОМОЛВЛЕН', 'ЖЕНАТ', 'В ГРАЖДАНСОКМ БРАКE', 'ВЛЮБЛЕН', 'ВСЕ СЛОЖНО', 'В АКТИВНОМ ПОИСКЕ']
        self.marital_status_female = ['НЕ ЗАМУЖЕМ', 'ВСТРЕЧАЮСЬ', 'ПОМОЛВЛЕНА', 'ЗАМУЖЕМ', 'В ГРАЖДАНСОКМ БРАКE', 'ВЛЮБЛЕНА', 'ВСЕ СЛОЖНО', 'В АКТИВНОМ ПОИСКЕ']
        self.result = []
        self.person_photos = ''
        self.person_count = 0
    
    # Метод, возвращающий username по id
    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id"+str(user_id))
        bs = BeautifulSoup(request.text, "html.parser")
        
        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])
        
        return user_name.split()[0]
    
    # Метод, возвращающий все параметры в изначальное состояние для нового поиска
    def return_standard_values(self):
        self.answers = {'marital_status' : []}
        self.person_count = 0
        self.keyboard['buttons'] = create_text_keyboard(['НАЧАТЬ'])
        self.person_photos = ''
        self.result = []
        self.count = 0
        self.function_variable = 0
        for el in self.control_field_occupancy:
            el = False
        
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
        result = VKUser(self._USER_ID, search_dict).search_people_by_users_search()
        return result
    # Метод, позволяющий написать пользователя сообщение
    def new_message(self, message):
        # Начало работы с ботом
        if self.control_field_occupancy['start'] == False and message.upper() == 'НАЧАТЬ':
            bot_answer = f"Привет, {self._USERNAME}! Я могу тебе помочь найти пару на всю жизнь! Ну или хорошую дружбу. Для начала, ты хочешь рассказать подробнее о нужном человеке? Если нет, то я сам подберу для тебя пару."
            self.keyboard['buttons'] = create_text_keyboard(['ДА', 'НЕТ'])
            self.control_field_occupancy['start'] = True

        # Получение ответов пользователя для отладки
        elif message == '!':
            self.print_answers()
            bot_answer = f'Написал твои ответы. Это нужно только для отладки :).'
            self.keyboard['buttons'] = []

        # Если пользователь согласен дать уточнения для поиска
        elif self.control_field_occupancy['correction'] == False and message.upper() == 'ДА':
            self.write_answer(True, 'correction')
            self.keyboard['buttons'] = create_text_keyboard(['МУЖЧИНУ', 'ДЕВУШКУ'])
            bot_answer = f"Хорошо. Тогда ответь на вопрос, ты ищешь мужчину или девушку?"
            self.control_field_occupancy['correction'] = True

        # Если пользователь не согласен дать уточнения для поиска. В таком случае основываемся на его данных из VK.com
        elif self.control_field_occupancy['correction'] == False and message.upper() == 'НЕТ':
            self.write_answer(False, 'correction')
            bot_answer = f'Напиши, сколько тебе лет?'
        #     bot_answer = f"Хорошо. Тогда ответь только на один вопрос, ты ищешь мужчину или девушку?"
            self.keyboard['buttons'] = []
            self.control_field_occupancy['correction'] = True

        # Если пользователю никто не понравился, то начинаем поиск заново
        elif message.upper() == 'НАЧАТЬ ПОИСК ЗАНОВО':
            self.answers = {'marital_status' : []}
            self.person_count = 0
            self.keyboard['buttons'] = create_text_keyboard(['НАЧАТЬ'])
            self.return_standard_values()
            bot_answer = f'Очень жаль, что тебе никто не понравился. Давай попробуем сначала:)'

        # Если пользователь согласилсяуточнить поиск
        elif self.answers['correction'] == True:
            # Пользователь выбирает мужчину или девушку
            if self.control_field_occupancy['sex'] == False and any(message.upper() == x for x in ['МУЖЧИНУ', 'ДЕВУШКУ']):
                if message.upper() =='МУЖЧИНУ':
                    self.write_answer('2', 'sex')
                else:
                    self.write_answer('1', 'sex')
                bot_answer = f"Миниальный возраст твоей половинки?"
                self.keyboard['buttons'] = []
                self.control_field_occupancy['sex'] = True

            # Пользователь вводит минимальный возраст
            elif self.control_field_occupancy['min_age'] == False and checking_number_in_str(message):
                if age_verification({'min_age': int(message)}):
                    self.write_answer(int(message), 'min_age')
                    bot_answer = f"Максимальный возраст твоей половинки? Он должен быть не больше {self.answers['min_age']}"
                    self.keyboard['buttons'] = []
                    self.control_field_occupancy['min_age'] = True
                else:
                    bot_answer = f"Минимальный возраст введен не верно. Должен быть больше 0. Введи верный возраст."

            # Пользователь вводит максимальный возраст
            elif self.control_field_occupancy['max_age'] == False and checking_number_in_str(message):
                if age_verification({'max_age': int(message)}, self.answers['min_age']):
                    self.write_answer(int(message), 'max_age')
                    bot_answer = f"В каком городе планируешь искать?"
                    self.keyboard['buttons'] = []
                    self.control_field_occupancy['max_age'] = True
                else:
                    bot_answer = f"Максимальный возраст должен быть больше {self.answers['min_age']}. Введи верный возраст."

            # Пользователь вводит город для поиска. Проверяем вхождение искомого города в списке городов, полученных из функции find_russia_cities
            elif self.control_field_occupancy['city'] == False and find_citi_in_VK(self._USER_ID, message.upper())  and self.count == 0:
                citi_list = find_citi_in_VK(self._USER_ID, message.upper())
                # Если при проверке города в ВК имеется несколько таких городов, то просим пользователя утчнить наименование города
                if isinstance(citi_list, list) and len(citi_list) > 1:
                    bot_answer = f"Найдено несколько мест:\n"
                    self.function_variable = []
                    for idx, city in enumerate(citi_list):
                        bot_answer += f"{idx + 1} - {city['region']}, {city['area']}, {city['title']} \n"
                        self.function_variable.append(idx + 1)
                    bot_answer += 'Выбери нужный город.'
                    self.keyboard['buttons'] = create_text_keyboard(self.function_variable)
                    self.write_answer(citi_list, 'city') 
                # Иначе записываем в ответы найденный город, содержащий id города и название
                else:
                    bot_answer = f"И последний вопрос. В каком семейном положении находится человек?"
                    if self.answers['sex'] == 'male':
                        self.keyboard['buttons'] = add_next_button(create_text_keyboard(self.marital_status_male))
                    else:
                        self.keyboard['buttons'] = add_next_button(create_text_keyboard(self.marital_status_female))   
                    self.control_field_occupancy['city'] = True  
                    self.write_answer(citi_list[0], 'city') 
                # Используем count для того, чтобы при нажатии на кнопку города в if программа не начала искать город по номеру кнопки
                self.count += 1
   
            # Если город уточнялся
            elif self.control_field_occupancy['city'] == False and int(message) in self.function_variable and self.answers['correction'] == True:
                self.answers['city'] = self.answers['city'][int(message) - 1]
                bot_answer = f"И последний вопрос. В каком семейном положении находится человек?" # Можешь выбрать несколько вариантов. Как закончишь, нажми кнопку 'Далее'.
                if self.answers['sex'] == 'male':
                    self.keyboard['buttons'] = add_next_button(create_text_keyboard(self.marital_status_male))
                else:
                    self.keyboard['buttons'] = add_next_button(create_text_keyboard(self.marital_status_female))
                self.control_field_occupancy['city'] = True

            # Даем пользователю возможность выбрать несколько статусов семейного положения
            # elif self.control_field_occupancy['marital_status'] == False and message.upper() in self.marital_status_male or message.upper() in self.marital_status_female:
            #     self.write_answer(message.upper(), 'marital_status')
            #     bot_answer = f"Продолжай:)."
            #     if self.answers['sex'] == 'male':
            #         self.keyboard['buttons'] = add_next_button(create_text_keyboard(self.marital_status_male))
            #     else:
            #         self.keyboard['buttons'] = add_next_button(create_text_keyboard(self.marital_status_female))

            # Пользователь вводит семейное положение. После чего начинается поиск.
            elif self.control_field_occupancy['marital_status'] == False and message.upper() in self.marital_status_male or message.upper() in self.marital_status_female:
                self.write_answer(message.upper(), 'marital_status')
                # Функция search_people ищет пользователей по всему ВК
                self.result = self.search_people()
                pprint(self.result)
                bot_answer = f"Нашли тебе {self.result['response']['count']} вариантов. Начнем смотреть?"
                self.keyboard['buttons'] = create_text_keyboard(['ДА', 'НЕТ'])
                self.control_field_occupancy['marital_status'] = True
            # Покажем пользователю количество пар, не превышающее self.result['response']['count']
            elif self.person_count < self.result['response']['count']:
                # Показываем пользователю первую пару
                if self.control_field_occupancy['person_1'] == False and message.upper() == 'ДА':
                    self.write_answer(message.upper(), 'person_1')
                    data = convert_data_for_message(self, 1)
                    self.control_field_occupancy['person_1'] = True
                    bot_answer = data['bot_answer']
                    self.person_photos = data['person_photos']
                    if self.person_count == self.result['response']['count'] - 1:
                        self.keyboard['buttons'] = create_text_keyboard(['НАЧАТЬ ПОИСК ЗАНОВО'])
                    else:
                        self.keyboard['buttons'] = create_text_keyboard(['ДАЛЕЕ'])
                    self.person_count += 1
                # Показываем пользователю вторую пару
                elif self.control_field_occupancy['person_2'] == False and message.upper() == 'ДАЛЕЕ':
                    self.write_answer(message.upper(), 'person_2')
                    data = convert_data_for_message(self, 2)
                    self.control_field_occupancy['person_2'] = True
                    bot_answer = data['bot_answer']
                    self.person_photos = data['person_photos']
                    if self.person_count == self.result['response']['count'] - 1:
                        self.keyboard['buttons'] = create_text_keyboard(['НАЧАТЬ ПОИСК ЗАНОВО'])
                    else:
                        self.keyboard['buttons'] = create_text_keyboard(['ДАЛЕЕ']) 
                    self.person_count += 1         
                # Показываем пользователю третью пару
                elif self.control_field_occupancy['person_3'] == False and message.upper() == 'ДАЛЕЕ':
                    self.write_answer(message.upper(), 'person_3')
                    data = convert_data_for_message(self, 3)
                    self.control_field_occupancy['person_3'] = True
                    bot_answer = data['bot_answer']
                    self.person_photos = data['person_photos']
                    self.keyboard['buttons'] = create_text_keyboard(['ДАЛЕЕ'])
                    self.person_count += 1
                # Показываем пользователю четвертую пару
                elif self.control_field_occupancy['person_4'] == False and message.upper() == 'ДАЛЕЕ':
                    self.write_answer(message.upper(), 'person_4')
                    data = convert_data_for_message(self, 4)
                    self.control_field_occupancy['person_4'] = True
                    bot_answer = data['bot_answer']
                    self.person_photos = data['person_photos']
                    if self.person_count == self.result['response']['count'] - 1:
                        self.keyboard['buttons'] = create_text_keyboard(['НАЧАТЬ ПОИСК ЗАНОВО'])
                    else:
                        self.keyboard['buttons'] = create_text_keyboard(['ДАЛЕЕ'])
                    self.person_count += 1
                # Показываем пользователю пятую пару
                elif self.control_field_occupancy['person_5'] == False and message.upper() == 'ДАЛЕЕ':
                    self.write_answer(message.upper(), 'person_5')
                    data = convert_data_for_message(self, 5)
                    self.control_field_occupancy['person_5'] = True
                    bot_answer = data['bot_answer']
                    self.person_photos = data['person_photos']
                    if self.person_count == self.result['response']['count'] - 1:
                        self.keyboard['buttons'] = create_text_keyboard(['НАЧАТЬ ПОИСК ЗАНОВО'])
                    else:
                        self.keyboard['buttons'] = create_text_keyboard(['ДАЛЕЕ'])
                    self.person_count += 1
                # Показываем пользователю шестую пару
                elif self.control_field_occupancy['person_6'] == False and message.upper() == 'ДАЛЕЕ':
                    self.write_answer(message.upper(), 'person_6')
                    data = convert_data_for_message(self, 6)
                    self.control_field_occupancy['person_6'] = True
                    bot_answer = data['bot_answer']
                    self.person_photos = data['person_photos']
                    if self.person_count == self.result['response']['count'] - 1:
                        self.keyboard['buttons'] = create_text_keyboard(['НАЧАТЬ ПОИСК ЗАНОВО'])
                    else:
                        self.keyboard['buttons'] = create_text_keyboard(['ДАЛЕЕ'])
                    self.person_count += 1
                # Показываем пользователю седьмую пару
                elif self.control_field_occupancy['person_7'] == False and message.upper() == 'ДАЛЕЕ':
                    self.write_answer(message.upper(), 'person_7')
                    data = convert_data_for_message(self, 7)
                    self.control_field_occupancy['person_7'] = True
                    bot_answer = data['bot_answer']
                    self.person_photos = data['person_photos']
                    if self.person_count == self.result['response']['count'] - 1:
                        self.keyboard['buttons'] = create_text_keyboard(['НАЧАТЬ ПОИСК ЗАНОВО'])
                    else:
                        self.keyboard['buttons'] = create_text_keyboard(['ДАЛЕЕ'])
                    self.person_count += 1
                # Показываем пользователю восьмую пару
                elif self.control_field_occupancy['person_8'] == False and message.upper() == 'ДАЛЕЕ':
                    self.write_answer(message.upper(), 'person_8')
                    data = convert_data_for_message(self, 8)
                    self.control_field_occupancy['person_8'] = True
                    bot_answer = data['bot_answer']
                    self.person_photos = data['person_photos']
                    if self.person_count == self.result['response']['count'] - 1:
                        self.keyboard['buttons'] = create_text_keyboard(['НАЧАТЬ ПОИСК ЗАНОВО'])
                    else:
                        self.keyboard['buttons'] = create_text_keyboard(['ДАЛЕЕ'])
                    self.person_count += 1
                # Показываем пользователю девятую пару
                elif self.control_field_occupancy['person_9'] == False and message.upper() == 'ДАЛЕЕ':
                    self.write_answer(message.upper(), 'person_9')
                    data = convert_data_for_message(self, 9)
                    self.control_field_occupancy['person_9'] = True
                    bot_answer = data['bot_answer']
                    self.person_photos = data['person_photos']
                    if self.person_count == self.result['response']['count'] - 1:
                        self.keyboard['buttons'] = create_text_keyboard(['НАЧАТЬ ПОИСК ЗАНОВО'])
                    else:
                        self.keyboard['buttons'] = create_text_keyboard(['ДАЛЕЕ'])
                    self.person_count += 1
                # Показываем пользователю десятую пару
                elif self.control_field_occupancy['person_10'] == False and message.upper() == 'ДАЛЕЕ':
                    self.write_answer(message.upper(), 'person_10')
                    data = convert_data_for_message(self, 10)
                    self.control_field_occupancy['person_10'] = True
                    bot_answer = data['bot_answer']
                    self.person_photos = data['person_photos']
                    self.keyboard['buttons'] = create_text_keyboard(['НАЧАТЬ ПОИСК ЗАНОВО'])
                    self.person_count += 1
                
        # Если пользователь не согласен дать уточнение по поиску, а хочет, чтобы бот сам нашел ему пару, то воспользуемся станадртными значениями:
        # пол - противоположный
        # возраст - +- 3 года от года рождения пользователя (если год рождения скрыт, попросим пользователя ввести его год рождения)
        # город - город пользователя
        # семейное положение - в активном поиске
        elif self.answers['correction'] == False:
            # if message.upper() == 'НЕТ':
                # bot_answer = f'Напиши, сколько тебе лет?'
                # self.control_field_occupancy['correction'] == True
            if self.control_field_occupancy['age'] == False and message.isdigit() :
                self.answers = {'marital_status' : ['6'],
                                'age' : message,
                                'sex' : opposite_sex(self._USER_SEX),
                                'min_age': int(message) - 3,
                                'max_age': int(message) + 3,
                                'city' : VKUser(self._USER_ID).find_city(),
                                'correction' : True,
                                }
                self.control_field_occupancy['marital_status'] = True
                self.control_field_occupancy['age'] = True
                self.control_field_occupancy['sex'] = True
                self.control_field_occupancy['min_age'] = True
                self.control_field_occupancy['max_age'] = True
                self.control_field_occupancy['city'] = True
                self.keyboard['buttons'] = create_text_keyboard(['ДА'])
                # Функция search_people ищет пользователей по всему ВК
                self.result = self.search_people()
                pprint(self.result)
                bot_answer = f"Нашли тебе {self.result['response']['count']} вариантов. Начнем смотреть?"
            # Покажем пользователю количество пар, не превышающее self.result['response']['count']
            elif self.person_count < self.result['response']['count']:
                # Показываем пользователю первую пару
                if self.control_field_occupancy['person_1'] == False and message.upper() == 'ДА':
                    self.write_answer(message.upper(), 'person_1')
                    data = convert_data_for_message(self, 1)
                    self.control_field_occupancy['person_1'] = True
                    bot_answer = data['bot_answer']
                    self.person_photos = data['person_photos']
                    if self.person_count == self.result['response']['count'] - 1:
                        self.keyboard['buttons'] = create_text_keyboard(['НАЧАТЬ ПОИСК ЗАНОВО'])
                    else:
                        self.keyboard['buttons'] = create_text_keyboard(['ДАЛЕЕ'])
                    self.person_count += 1
                # Показываем пользователю вторую пару
                elif self.control_field_occupancy['person_2'] == False and message.upper() == 'ДАЛЕЕ':
                    self.write_answer(message.upper(), 'person_2')
                    data = convert_data_for_message(self, 2)
                    self.control_field_occupancy['person_2'] = True
                    bot_answer = data['bot_answer']
                    self.person_photos = data['person_photos']
                    if self.person_count == self.result['response']['count'] - 1:
                        self.keyboard['buttons'] = create_text_keyboard(['НАЧАТЬ ПОИСК ЗАНОВО'])
                    else:
                        self.keyboard['buttons'] = create_text_keyboard(['ДАЛЕЕ']) 
                    self.person_count += 1         
                # Показываем пользователю третью пару
                elif self.control_field_occupancy['person_3'] == False and message.upper() == 'ДАЛЕЕ':
                    self.write_answer(message.upper(), 'person_3')
                    data = convert_data_for_message(self, 3)
                    self.control_field_occupancy['person_3'] = True
                    bot_answer = data['bot_answer']
                    self.person_photos = data['person_photos']
                    self.keyboard['buttons'] = create_text_keyboard(['ДАЛЕЕ'])
                    self.person_count += 1
                # Показываем пользователю четвертую пару
                elif self.control_field_occupancy['person_4'] == False and message.upper() == 'ДАЛЕЕ':
                    self.write_answer(message.upper(), 'person_4')
                    data = convert_data_for_message(self, 4)
                    self.control_field_occupancy['person_4'] = True
                    bot_answer = data['bot_answer']
                    self.person_photos = data['person_photos']
                    if self.person_count == self.result['response']['count'] - 1:
                        self.keyboard['buttons'] = create_text_keyboard(['НАЧАТЬ ПОИСК ЗАНОВО'])
                    else:
                        self.keyboard['buttons'] = create_text_keyboard(['ДАЛЕЕ'])
                    self.person_count += 1
                # Показываем пользователю пятую пару
                elif self.control_field_occupancy['person_5'] == False and message.upper() == 'ДАЛЕЕ':
                    self.write_answer(message.upper(), 'person_5')
                    data = convert_data_for_message(self, 5)
                    self.control_field_occupancy['person_5'] = True
                    bot_answer = data['bot_answer']
                    self.person_photos = data['person_photos']
                    if self.person_count == self.result['response']['count'] - 1:
                        self.keyboard['buttons'] = create_text_keyboard(['НАЧАТЬ ПОИСК ЗАНОВО'])
                    else:
                        self.keyboard['buttons'] = create_text_keyboard(['ДАЛЕЕ'])
                    self.person_count += 1
                # Показываем пользователю шестую пару
                elif self.control_field_occupancy['person_6'] == False and message.upper() == 'ДАЛЕЕ':
                    self.write_answer(message.upper(), 'person_6')
                    data = convert_data_for_message(self, 6)
                    self.control_field_occupancy['person_6'] = True
                    bot_answer = data['bot_answer']
                    self.person_photos = data['person_photos']
                    if self.person_count == self.result['response']['count'] - 1:
                        self.keyboard['buttons'] = create_text_keyboard(['НАЧАТЬ ПОИСК ЗАНОВО'])
                    else:
                        self.keyboard['buttons'] = create_text_keyboard(['ДАЛЕЕ'])
                    self.person_count += 1
                # Показываем пользователю седьмую пару
                elif self.control_field_occupancy['person_7'] == False and message.upper() == 'ДАЛЕЕ':
                    self.write_answer(message.upper(), 'person_7')
                    data = convert_data_for_message(self, 7)
                    self.control_field_occupancy['person_7'] = True
                    bot_answer = data['bot_answer']
                    self.person_photos = data['person_photos']
                    if self.person_count == self.result['response']['count'] - 1:
                        self.keyboard['buttons'] = create_text_keyboard(['НАЧАТЬ ПОИСК ЗАНОВО'])
                    else:
                        self.keyboard['buttons'] = create_text_keyboard(['ДАЛЕЕ'])
                    self.person_count += 1
                # Показываем пользователю восьмую пару
                elif self.control_field_occupancy['person_8'] == False and message.upper() == 'ДАЛЕЕ':
                    self.write_answer(message.upper(), 'person_8')
                    data = convert_data_for_message(self, 8)
                    self.control_field_occupancy['person_8'] = True
                    bot_answer = data['bot_answer']
                    self.person_photos = data['person_photos']
                    if self.person_count == self.result['response']['count'] - 1:
                        self.keyboard['buttons'] = create_text_keyboard(['НАЧАТЬ ПОИСК ЗАНОВО'])
                    else:
                        self.keyboard['buttons'] = create_text_keyboard(['ДАЛЕЕ'])
                    self.person_count += 1
                # Показываем пользователю девятую пару
                elif self.control_field_occupancy['person_9'] == False and message.upper() == 'ДАЛЕЕ':
                    self.write_answer(message.upper(), 'person_9')
                    data = convert_data_for_message(self, 9)
                    self.control_field_occupancy['person_9'] = True
                    bot_answer = data['bot_answer']
                    self.person_photos = data['person_photos']
                    if self.person_count == self.result['response']['count'] - 1:
                        self.keyboard['buttons'] = create_text_keyboard(['НАЧАТЬ ПОИСК ЗАНОВО'])
                    else:
                        self.keyboard['buttons'] = create_text_keyboard(['ДАЛЕЕ'])
                    self.person_count += 1
                # Показываем пользователю десятую пару
                elif self.control_field_occupancy['person_10'] == False and message.upper() == 'ДАЛЕЕ':
                    self.write_answer(message.upper(), 'person_10')
                    data = convert_data_for_message(self, 10)
                    self.control_field_occupancy['person_10'] = True
                    bot_answer = data['bot_answer']
                    self.person_photos = data['person_photos']
                    self.keyboard['buttons'] = create_text_keyboard(['НАЧАТЬ ПОИСК ЗАНОВО'])
                    self.person_count += 1
        else:
            bot_answer = f'Я вас не понимаю'

        return {'message' : bot_answer, 'keyboard' : self.keyboard, 'mediafile' : self.person_photos}

        