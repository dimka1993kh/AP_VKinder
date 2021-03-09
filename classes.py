import requests
import time
from pprint import pprint

class VKUser():
    def __init__(self, user_id, search:dict=None):
        self.user_id = user_id
        self.access_token = "95614099d2eb0b8dc02b9851821f30c1fd0cfa0c54aa7def33fc39ddaf8bd7209de4b588567878ce01117"
        self.api_urls_get = 'https://api.vk.com/method/users.get'
        self.api_urls_search = 'https://api.vk.com/method/users.search'
        self.search = search
# Запишем параметры для конкретного запроса
        self.params_get = {
            'user_id' :  self.user_id, 
            'fields' : 'sex',
            'access_token' : self.access_token,
            'v' : '5.126',
        }
# Параметры для поиска
        if search:
            self.params_search = {
                'count' :  '10', 
                'sex' : self.search['sex'],
                'status' : self.search['status'],
                'age_from' : self.search['age_from'],
                'age_to' : self.search['age_to'], 
                'has_photo' : '1',
                'city' : self.search['city'], 

                'access_token' : self.access_token,
                'v' : '5.126',
            }        
# Метод поиска пола пользователя
    def find_sex(self):
        resp = requests.get(self.api_urls_get, params=self.params_get)
        resp.raise_for_status()
        return resp.json()['response'][0]['sex'] 
# Метод поиска пар  
    def search_pepople(self):
        resp = requests.get(self.api_urls_search, params=self.params_search)
        resp.raise_for_status()
        return resp.json()



# семейное положение. Возможные значения:
# 1 — не женат (не замужем);
# 2 — встречается;
# 3 — помолвлен(-а);
# 4 — женат (замужем);
# 5 — всё сложно;
# 6 — в активном поиске;
# 7 — влюблен(-а);
# 8 — в гражданском браке.
search_dict = {
            'sex' : 1,
            'status' : 1,
            'age_from' : 18,
            'age_to' : 30,
            'city' : 2
        }

fff = VKUser('23890940', search_dict).search_pepople()
pprint(fff)
print(len(fff['response']['items']))
for i in fff['response']['items']:
    pprint('https://vk.com/id' + str(i['id']))