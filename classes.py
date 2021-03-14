import requests
import time
from datetime import date
from pprint import pprint
from token_data import user_access_token

class VKUser():
    def __init__(self, user_id, search:dict=None, user_access_token:str=user_access_token):
        self.user_id = user_id
        self.user_access_token = user_access_token
        self.api_urls_get = 'https://api.vk.com/method/users.get'
        self.api_urls_search = 'https://api.vk.com/method/users.search'
        self.api_urls_search_cities = 'https://api.vk.com/method/database.getCities'
        self.api_photos = 'https://api.vk.com/method/photos.get'
        self.api_get_friends = 'https://api.vk.com/method/friends.get' 
        self.api_urls_search_in_friends = 'https://api.vk.com/method/friends.search'  
        self.search = search
# Запишем параметры для конкретного запроса
        self.params_get = {
            'user_ids' :  f'{self.user_id}', 
            'fields' : 'sex, city',
            'access_token' : self.user_access_token,
            'v' : '5.126',
        }
# Параметры для поиска списка всех городов
        self.params_search_cities = {
            'country_id' : '1', # Россия
            'need_all' : '1',
            'count' : '1000',
            'access_token' : self.user_access_token,
            'v' : '5.130',
        } 
# Параметры для поиска конкретного города
        self.params_search_cities = {
            'country_id' : '1', # Россия
            'count' : '1000',
            'access_token' : self.user_access_token,
            'v' : '5.130',
        } 
# Параметры для поиска друзей
        self.params_get_friends = {
                        'count' : '5000',
                        'can_access_closed ' : '1', 
                        'access_token' : self.user_access_token,
                        'v' : '5.89',
                    }





# Параметры для получения фотографий профиля определенного пользователя
        self.params_get_photos = {
            'album_id' : 'profile', 
            'extended' : '1',
            'photo_sizes' : '1',
            'count' : '1000',

            'access_token' : self.user_access_token,
            'v' : '5.130',
        } 
# Параметры для поиска
        if self.search:
            self.params_search = {
                'user_id' : f"{self.user_id}",
                'count' :  '1000', 
                'sex' : self.search['sex'],
                'status' : self.search['status'],
                'age_from' : self.search['age_from'],
                'age_to' : self.search['age_to'], 
                'has_photo' : '1',
                'city' : self.search['city'], 
                'fields' : 'country, city',
                'can_access_closed ' : '1', 
                'access_token' : self.user_access_token,
                'v' : '5.130',
            }
        else:
            self.params_search = {}  
     
# Метод поиска пола пользователя
    def find_sex(self):
        resp = requests.get(self.api_urls_get, params=self.params_get)
        resp.raise_for_status()
        return resp.json()['response'][0]['sex']
    
    def find_city(self):
        resp = requests.get(self.api_urls_get, params=self.params_get)
        resp.raise_for_status()
        return resp.json()['response'][0]['city']


# Метод поиска по users.search
    def search_people_by_users_search(self, removable_urls:list=None):
        # Поиск подходящих людей по всему интернету, не объективен
        count = 0
        result = {'response': {'count' : count, 'items' : []}}
        info_list = ['first_name', 'last_name', 'country', 'city', 'src', 'top_photo']
        resp = requests.get(self.api_urls_search, params=self.params_search)
        resp.raise_for_status()
        for person in resp.json()['response']['items']:
            url = self.get_person_url(person['id'])
            photo = self.get_top_photo(person['id'])
            # Если полученный url пользователя находится в исключаемых url - его не записываем
            if url in removable_urls or photo == False:
                continue
            else:
                if count < 10:
                    person_result = {}
                    for el in info_list:
                        if el == 'src':
                            person_result[el] = url
                        elif el == 'top_photo':
                            person_result[el] = photo
                        elif el in person.keys():
                            person_result[el] = person[el]
                    count += 1
                    # print('person_result', person_result)
                    result['response']['items'].append(person_result)
                else:
                    break
        result['response']['count'] = len(result['response']['items'])
        return result
# Метод поиска пар  
    def search_pepople(self):

        # Поиск будем весьи следующим образом:
        # Найдем всех друзей пользователя (если они закрыты, предупредим пользователя, что поиск будет вестись по всему ВК, что усложнит поис ПОДХОДЯЩЕЙ пары)
        # У каждого друга найдем всех друзей по заданным параметрам ( таким образом обеспечим пользователю доступ к друзьям друзей, близкий круг общения)
        # Если этого окажется мало, можно капнуть еще глубже - в друзья друзей друзей

        result = {'response': {'items' : []}}
        info_list = ['first_name', 'last_name', 'country', 'city', 'src', 'top_photo']
        resp = requests.get(self.api_urls_search, params=self.params_search)
        resp.raise_for_status()
        friends_ids = self.get_friends_ids()
        all_friends_friends = []
        for el in friends_ids:
            time.sleep(0.5)
            for person in VKUser(str(el), self.search).search_pepople_in_friends():
                all_friends_friends.append(person)

        for person in all_friends_friends:
            person_result = {}
            for el in info_list:
                if el in person.keys():
                    person_result[el] = person[el]
                elif el == 'src':
                    person_result[el] = self.get_person_url(person['id'])
                elif el == 'top_photo':
                    person_result[el] = self.get_top_photo(person['id'])
            result['response']['items'].append(person_result)
        return result









    # result = { 'response' : {'items' : [{'first_name' : ...,
    #                                     'last_name' : ...,
    #                                     'country' : ...,
    #                                     'city' : ...,
    #                                     'src' : ...,
    #                                     'top_photo' : [...,
    #                                                     ...,
    #                                                     ...,
    #                                                     ]
    #                                     }]
    #                         }
    #         }

    def get_friends_ids(self):
        result = []
        additional_params = {'offset' :  0,}
        num_offset = 5000
        while num_offset == 5000:
            resp = requests.get(self.api_get_friends, params=self.params_get_friends | additional_params)
            resp.raise_for_status() 
            for user_id in resp.json()['response']['items']:
                result.append(user_id)
            num_offset = resp.json()['response']['count']
        return result
# Поиск по параметрам среди друзей
    def search_pepople_in_friends(self):
        result = []
        resp = requests.get(self.api_urls_search_in_friends, params=self.params_search)
        resp.raise_for_status()
        print(resp.json())
        # print(resp.json())
        for el in resp.json()['response']['items']:
            if 'error' not in el.keys():
                result.append(el)
            print(el)
        return result

# Метод получения ссылки на профиль
    def get_person_url(self, person_id):
        url_part = 'https://vk.com/id'
        result = url_part + str(person_id)
        return result
# Метод получения фотографий определенного пользователя
    def get_top_photo(self, user_id):
        time.sleep(0.5)
        result = []
        additional_params = {'owner_id' : user_id}
        resp = requests.get(self.api_photos, params=self.params_get_photos | additional_params)
        resp.raise_for_status() 
        # print(resp.json())
        if 'error' in resp.json().keys() and resp.json()['error']['error_code'] == 30:
            return False
        else:
            photos = resp.json()['response']['items']
            photos.sort(key=lambda photo: photo['likes']['count'], reverse = True)
            for photo in photos[:3]:
                result.append({'user_id' : user_id, 'photo_id': photo['id'] ,'src' : photo['sizes'][-1]['url']})
        return result

# Поиск всех городов
    def search_cities(self, params):
        resp = requests.get(self.api_urls_search_cities, params=self.params_search_cities | params)
        resp.raise_for_status() 
        return resp.json()

# Поиск конкретного города
    def search_citi(self, params):
        resp = requests.get(self.api_urls_search_cities, params=self.params_search_cities | params)
        resp.raise_for_status() 
        return resp.json()




search_dict = {
    'sex' : '1',
    'status' : '6',
    'age_from' : '20',
    'age_to' : '30',
    'city' : '2'
}


# fff = VKUser('27771889', search_dict).calculateAge()
# pprint(fff)

# for el in fff:
#     print(el['likes']['count'])

# fff = VKUser('27771889', search_dict).search_pepople_in_friends()
# pprint(fff)



