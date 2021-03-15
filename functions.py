from bs4 import BeautifulSoup
import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import re
import math
import time
from sqlalchemy.sql.expression import func



# Проверка возраста
def age_verification(dict_age:dict, min_age:int=None):
    if min_age and list(dict_age.keys())[0] == 'max_age':
        if dict_age['max_age'] >= min_age:
            return True
        else:
            return False 
    elif list(dict_age.keys())[0] == 'min_age':
        if dict_age['min_age'] > 0:
            return True
        else:
            return False 

# Функция для преобразовывания полученных данных о людях, для передачи этих данных в сообщении пользователя (фото, имя, фамилия, город и т.д.)
def convert_data_for_message(object_vk_bot, number_person:int):
    number_person = number_person - 1 
    bot_answer = f"{object_vk_bot.result['response']['items'][number_person]['first_name']} {object_vk_bot.result['response']['items'][number_person]['last_name']} \n {object_vk_bot.result['response']['items'][number_person]['src']}"
    person_photos = ''
    for photo in object_vk_bot.result['response']['items'][number_person]['top_photo']:
        person_photos += f"photo{photo['user_id']}_{photo['photo_id']},"
    return {'bot_answer' : bot_answer, 'person_photos' : person_photos}

# Функция для определения цвета кнопки бота
def analize_color_button(color):
    if color == 'NEGATIVE':
        result = VkKeyboardColor.NEGATIVE
    elif color == 'POSITIVE':
        result = VkKeyboardColor.POSITIVE
    elif color == 'PRIMARY':
        result = VkKeyboardColor.PRIMARY
    elif color == 'SECONDARY':
        result = VkKeyboardColor.SECONDARY
    return result

# Функция определения последнего id а таблице bd
def max_id_in_db(session, db):
    # Определим индекс последнего элемента в db
    max_id_in_db = session.query(func.max(db.id)).first()[0]
    if max_id_in_db:
        max_id = max_id_in_db + 1
    else:
        max_id = 1
    return max_id


# Функция поиска городов россии
    # def find_russia_cities(user_id):
    #     result = []
    #     while_condition = 1000
    #     params_search_cities = {
    #                             'offset' : 0,
    #                             }
    #     user = VKUser(user_id)    
    #     while while_condition == 1000:
    #         time.sleep(0.2)
    #         cities_dict = user.search_cities(params_search_cities)['response']['items']
    #         for citi in cities_dict:
    #             citi_info = {}
    #             citi_info['id'] = citi['id']
    #             citi_info['title'] = citi['title'].upper()
    #             result.append(citi_info)
    #         params_search_cities['offset'] += len(cities_dict)
    #         while_condition = len(cities_dict)
    #     return result

# Функция поиска города в вк
    # def find_citi_in_VK(user_id, citi):
    #     user = VKUser(user_id)
    #     params = {'q' : citi}
    #     citi = user.search_cities(params)
    #     if 'error' not in citi:
    #         citi = citi['response']['items']
    #     elif citi['error']['error_code'] == 100:
    #         citi = False
    #     return citi

# Функция проверки вхождения города в список городов
    # def checking_city_entries(input_citi:str, func:dict):
    #     for citi in func:
    #         if input_citi in citi['title']:
    #             return {'check' : True,
    #                     'citi_info' : citi
    #                     }

# Проверка написания в строке числа    
    # def checking_number_in_str(input_str:str):
    #     if input_str.isdigit():
    #         return True
    #     elif input_str[0] == '-' and input_str[1:].isdigit():
    #         return True
    #     else:
    #         return False

# Функция получения пола пользователя
    # def get_user_sex(user_id):
    #     sex = VKUser(user_id).find_sex()
    #     return sex

# Функция, возвращаяюшаяя обратный пол пользователя
    # def opposite_sex(user_sex):
        # if user_sex == 1:
        #     return '2'
        # elif user_sex == 2:
        #     return '1'
        # else:
        #     raise Exception('Введен невенрый пол. Должно быть значение 1 (ж) или 2 (м)')







    
