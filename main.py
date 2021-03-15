import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from classes import VkBot
from random import randrange
import json
from pprint import pprint
from token_data import group_token


if __name__ == '__main__':
    
    def write_msg(user_id, result):
        vk.method('messages.send', {'user_id': user_id, 'message': result['message'], 'random_id': randrange(10 ** 7), 'command' : 'start', 'keyboard' : result['keyboard'], 'attachment' : result['mediafile']})

    # Авторизуемся как сообщество
    vk = vk_api.VkApi(token=group_token)

    # Работа с сообщениями
    longpoll = VkLongPoll(vk)

    # Основной цикл
    users = {

    }
    print("Server started")
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                if str(event.user_id) not in list(users.keys()):
                    users[f'{event.user_id}'] = VkBot(event.user_id)
                write_msg(event.user_id, users[f'{event.user_id}'].new_message(event.text))