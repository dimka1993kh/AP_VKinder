from bs4 import BeautifulSoup
import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import re
import math
from pprint import pprint
from classes import VKUser
import time

def find_russia_cities(user_id):
    result = []
    while_condition = 1000
    params_search_cities = {
                            'offset' : 0,
                            }
    user = VKUser(user_id)    
    while while_condition == 1000:
        time.sleep(0.2)
        cities_dict = user.search_cities(params_search_cities)['response']['items']
        for citi in cities_dict:
            citi_info = {}
            citi_info['id'] = citi['id']
            citi_info['title'] = citi['title'].upper()
            result.append(citi_info)
        params_search_cities['offset'] += len(cities_dict)
        while_condition = len(cities_dict)
    return result


def find_citi_in_VK(user_id, citi):
    user = VKUser(user_id)
    params = {'q' : citi}
    citi = user.search_cities(params)
    if 'error' not in citi:
        citi = citi['response']['items']
    elif citi['error']['error_code'] == 100:
        citi = False
    return citi



def checking_city_entries(input_citi:str, func:dict):
    for citi in func:
        if input_citi in citi['title']:
            return {'check' : True,
                    'citi_info' : citi
                    }
    # responce = requests.get('https://pynop.com/goroda.htm')
    # responce.raise_for_status()
    # responce.encoding = 'cp1251'
    # soup = BeautifulSoup(responce.text, features="html.parser")

    # data = soup.findAll('p', class_='MsoNormal')
    # result = []
    # for el in data:
    #     city = re.match(r"\D+", el.text.split()[0])
    #     if city:
    #         result.append(city.group(0).upper())
    # return result[: -2]
# Параметры для поиска списка всех городов
        

def create_text_keyboard(label_list: list):
    rows = math.ceil(len(label_list) / 4) 
    num_buttons_on_row = 0
    row_result = []
    result = []
    for idx, label in enumerate(label_list):
        if num_buttons_on_row < 4:
            num_buttons_on_row += 1
            row_result.append({
                            "action":{
                                        "type":"text",
                                        "label":f"{label}"
                                        }
                            }) 
        if num_buttons_on_row == 4:
            num_buttons_on_row = 0
            result.append(row_result)
            row_result = []
        elif idx == len(label_list) - 1:
            result.append(row_result)
    return result

def add_next_button(func: list):
    result = func
    result.append([{
                "action":{
                        "type":"text",
                        "label":"Далее"
                        }
                }])
    return result

# dict_age = {'min_age' : int}
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
    

def checking_number_in_str(input_str:str):
    if input_str.isdigit():
        return True
    elif input_str[0] == '-' and input_str[1:].isdigit():
        return True
    else:
        return False



def get_user_sex(user_id):
    sex = VKUser(user_id).find_sex()
    # if sex == 1:
    #     return 'fimale'
    # elif sex == 2:
    #     return 'male'
    return sex

def opposite_sex(user_sex):
    print('user_sex', user_sex)
    if user_sex == 1:
        return '2'
    elif user_sex == 2:
        return '1'
    else:
        raise Exception('Введен невенрый пол. Должно быть значение 1 (ж) или 2 (м)')

# Функция для преобразовывания полученных данных о людях, для передачи этих данных в сообщении пользователя (фото, имя, фамилия, город и т.д.)
def convert_data_for_message(object_vk_bot, number_person:int):
    number_person = number_person - 1 
    bot_answer = f"{object_vk_bot.result['response']['items'][number_person]['first_name']} {object_vk_bot.result['response']['items'][number_person]['last_name']} \n {object_vk_bot.result['response']['items'][number_person]['src']}"
    person_photos = ''
    for photo in object_vk_bot.result['response']['items'][number_person]['top_photo']:
        person_photos += f"photo{photo['user_id']}_{photo['photo_id']},"
    return {'bot_answer' : bot_answer, 'person_photos' : person_photos}



# print(find_russia_cities('23890940'))




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
    
