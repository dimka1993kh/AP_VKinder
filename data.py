empty_keyboard = {
    "one_time": False,
    "buttons": []
}


# possible_answers = { <Номер вопроса> : { <Ключ поля в self.answers> : <Значение поля в self.answers>,
#                                         <Сообщение> : <type str or None>,
#                                         <Сообщение является числом?> : <True or False>,
#                                         <Номер следующего вопроса> : <type int>
#                                         <Ответ бота> : <type str>,
#                                         <Клавиатура> : <False or [[<Наименование кнопки>, <Цвет кнопки>], ...]>
#                                           },
#                                         
#                   }



# possible_answers = {'1' : [{'write_to_answers' : {'correction' : False},
#                             'message': 'НЕТ',
#                             'message_is_digit' : False,
#                             'next_question' : 2,
#                             'bot_answer': f'Напиши, сколько тебе лет?',
#                             'keyboard' : False,
#                             },
#                             {'write_to_answers' : {'correction' : True},
#                             'message': 'ДА',
#                             'message_is_digit' : False,
#                             'next_question' : 3,
#                             'bot_answer': f'Хорошо. Тогда ответь на вопрос, ты ищешь мужчину или девушку?',
#                             'keyboard' : [['Мужчину', 'POSITIVE'], ['Девушку', 'POSITIVE']],
#                             }],
#                     '2' : {'write_to_answers' : False,
#                             'message': None,
#                             'message_is_digit' : True,
#                             'next_question' : 100,
#                             'bot_answer': f"Нашли тебе {self.result['response']['count']} вариантов. Начнем смотреть?",
#                             'keyboard' : [['Мужчину', 'POSITIVE'], ['Девушку', 'POSITIVE']],
#                             },
                        
#                     }