from bs4 import BeautifulSoup
import requests
import re
import math
from pprint import pprint

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
