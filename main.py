import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_bot import VkBot
from random import randrange
import json
from pprint import pprint
from token import group_token

if __name__ == '__main__':
    
    def write_msg(user_id, result):
        pprint(result['keyboard'])
        vk.method('messages.send', {'user_id': user_id, 'message': result['message'], 'random_id': randrange(10 ** 7), 'command' : 'start', 'keyboard' : json.dumps(result['keyboard']), 'attachment' : result['mediafile']})


    # Авторизуемся как сообщество
    vk = vk_api.VkApi(token=group_token)

    # Работа с сообщениями
    longpoll = VkLongPoll(vk)

    # Основной цикл
    my_dict = {

    }
    print("Server started")
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                print('New message:')
                print(f'For me by: {event.user_id}', end='')
                if str(event.user_id) not in list(my_dict.keys()):
                    my_dict[f'{event.user_id}'] = VkBot(event.user_id)
                write_msg(event.user_id, my_dict[f'{event.user_id}'].new_message(event.text))
                
                print('Text: ', event.text)