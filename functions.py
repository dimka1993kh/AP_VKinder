from bs4 import BeautifulSoup
import requests
import re
import math
from pprint import pprint
from classes import VKUser

def find_russia_cities():
    responce = requests.get('https://pynop.com/goroda.htm')
    responce.raise_for_status()
    responce.encoding = 'cp1251'
    soup = BeautifulSoup(responce.text, features="html.parser")

    data = soup.findAll('p', class_='MsoNormal')
    result = []
    for el in data:
        city = re.match(r"\D+", el.text.split()[0])
        if city:
            result.append(city.group(0).upper())
    return result[: -2]


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


