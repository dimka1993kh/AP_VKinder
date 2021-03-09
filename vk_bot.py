import requests
from bs4 import BeautifulSoup
from data import cities
from functions import create_text_keyboard, add_next_button, age_verification, checking_number_in_str, get_user_sex
from classes import VKUser









class VkBot:
    def __init__(self, user_id):
        print("Создан объект бота!")
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)
        self._USER_SEX = get_user_sex(self._USER_ID)
        self.answers = {'marital_status' : []}
        self.count = 0
        self.keyboard = {
                            "one_time":False,
                            "buttons":[],
                            "inline" : False
                        }
        self.marital_status_male = ['НЕ ЖЕНАТ', 'ВСТРЕЧАЮСЬ', 'ПОМОЛВЛЕН', 'ЖЕНАТ', 'В ГРАЖДАНСОКМ БРАКE', 'ВЛЮБЛЕН', 'ВСЕ СЛОЖНО', 'В АКТИВНОМ ПОИСКЕ']
        self.marital_status_female = ['НЕ ЗАМУЖЕМ', 'ВСТРЕЧАЮСЬ', 'ПОМОЛВЛЕНА', 'ЗАМУЖЕМ', 'В ГРАЖДАНСОКМ БРАКE', 'ВЛЮБЛЕНА', 'ВСЕ СЛОЖНО', 'В АКТИВНОМ ПОИСКЕ']
    
    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id"+str(user_id))
        bs = BeautifulSoup(request.text, "html.parser")
        
        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])
        
        return user_name.split()[0]
        
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
    
    def write_answer(self, message, question_name):
        if question_name in self.answers.keys() and isinstance(self.answers[question_name], list):
            self.answers[question_name].append(message)
        else:
            self.answers[question_name] = message
    
    def print_answers(self):
        print('Ответы', self.answers)

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

    def search_people(self):
        search_dict = {
            'sex' : self._USER_SEX,
            'status' : self.convert_status(),
            'age_from' : self.answers['min_age'],
            'age_to' : self.answers['max_age'],
        }
        result = VKUser(self._USER_ID, search_dict).search_pepople()
        return result

    def new_message(self, message):
        # Начало работы с ботом
        if message.upper() == 'НАЧАТЬ':
            bot_answer = f"Привет, {self._USERNAME}! Я могу тебе помочь найти пару на всю жизнь! Ну или хорошую дружбу. Для начала, ты хочешь рассказать подробнее о нужном человеке? Если нет, то я сам подберу для тебя пару."
            self.keyboard['buttons'] = create_text_keyboard(['ДА', 'НЕТ'])
        # Получение ответов пользователя для отладки
        elif message == '!':
            self.print_answers()
            bot_answer = f'Написал твои ответы. Это нужно только для отладки :).'
            self.keyboard['buttons'] = []
        # Если пользователь согласен дать уточнения для поиска
        elif message.upper() == 'ДА':
            self.write_answer(True, 'correction')
            self.keyboard['buttons'] = create_text_keyboard(['МУЖЧИНУ', 'ДЕВУШКУ'])
            bot_answer = f"Хорошо. Тогда ответь на вопрос, ты ищешь мужчину или девушку?"
        # Если пользователь не согласен дать уточнения для поиска. В таком случае основываемся на его данных из VK.com
        elif message.upper() == 'НЕТ':
            self.write_answer(False, 'correction')
            bot_answer = f"Хорошо. Тогда ответь только на один вопрос, ты ищешь мужчину или девушку?"
            self.keyboard['buttons'] = create_text_keyboard(['МУЖЧИНУ', 'ДЕВУШКУ'])
        # Пользователь выбирает мужчину или девушку
        elif any(message.upper() == x for x in ['МУЖЧИНУ', 'ДЕВУШКУ'])  and self.answers['correction'] == True:
            if message.upper() =='МУЖЧИНУ':
                self.write_answer('male', 'sex')
            else:
                self.write_answer('female', 'sex')
            bot_answer = f"Миниальный возраст твоей половинки?"
            self.keyboard['buttons'] = []
        # Пользователь вводит минимальный возраст
        elif checking_number_in_str(message) and self.count == 0 and self.answers['correction'] == True:
            if age_verification({'min_age': int(message)}):
                self.write_answer(int(message), 'min_age')
                bot_answer = f"Максимальный возраст твоей половинки? Он должен быть не больше {self.answers['min_age']}"
                self.keyboard['buttons'] = []
                self.count += 1
            else:
                bot_answer = f"Минимальный возраст введен не верно. Должен быть больше 0. Введи верный возраст."
        # Пользователь вводит максимальный возраст
        elif checking_number_in_str(message) and self.count == 1 and self.answers['correction'] == True:
            if age_verification({'max_age': int(message)}, self.answers['min_age']):
                self.write_answer(int(message), 'max_age')
                bot_answer = f"В каком городе планируешь искать?"
                self.keyboard['buttons'] = []
            else:
                bot_answer = f"Максимальный возраст должен быть больше {self.answers['min_age']}. Введи верный возраст."
        # Пользователь вводит город для поиска. Проверяем вхождение искомого города в списке городов, полученных из функции find_russia_cities
        elif message.upper() in cities and self.answers['correction'] == True:
            self.write_answer(message.upper(), 'citi')
            bot_answer = f"И последний вопрос. В каком семейном положении находится человек? Можешь выбрать несколько вариантов. Как закончишь, нажми кнопку 'Далее'."
            if self.answers['sex'] == 'male':
                self.keyboard['buttons'] = add_next_button(create_text_keyboard(self.marital_status_male))
            else:
                self.keyboard['buttons'] = add_next_button(create_text_keyboard(self.marital_status_female))
        # Даем пользователю возможность выбрать несколько статусов семейного положения
        elif message.upper() in self.marital_status_male or message.upper() in self.marital_status_female:
            self.write_answer(message.upper(), 'marital_status')
            bot_answer = f"Продолжай:)."
            if self.answers['sex'] == 'male':
                self.keyboard['buttons'] = add_next_button(create_text_keyboard(self.marital_status_male))
            else:
                self.keyboard['buttons'] = add_next_button(create_text_keyboard(self.marital_status_female))

        # Пользователь вводит семейное положение. После чего начинается поиск.
        elif message.upper() == 'ДАЛЕЕ' or self.answers['correction'] == False:
            bot_answer = f"Идет поиск, сейчас найдем тебе кандидатов:)"
            people = self.search_people()
            print(people)
            self.keyboard['buttons'] = []

        else:
            bot_answer = f'Я вас не понимаю'

        return {'message' : bot_answer, 'keyboard' : self.keyboard}
        # # Соглашается дать уточнения
        # if message.upper() == self._COMMANDS[1]:
        #     self.write_answer(message, 'correction')
        #     return f"Отлично! Напиши минимальный возраст твоей второй половинки."

        # # Минимальный возраст
        # if message.upper() == self._COMMANDS[1]:
        #     self.write_answer(message, 'correction')
        #     return f"Отлично! Напиши минимальный возраст твоей второй половинки."

        # # Напечатать ответы
        # if message.upper() == self._COMMANDS[2]:
        #     self.print_answers()
        #     return f'Написал твои ответы, посмотри'



        # else:
        #     return "Не понимаю о чем вы..."

        