from token_data import user_access_token
from classes import VKUser, VkBot
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from db.main import Base, engine
from sqlalchemy.orm import sessionmaker
from db.models import User, VkinderResult

test_id = '23890940'
test_id_female = '27771889'

class TestVKUser:
        
    def setup(self):
        print("method setup")   
    def teardown(self):
        print("method teardown") 


    def test_find_sex(self):
        test_user = VKUser(test_id)
        assert test_user.find_sex() == 2
    
    def test_find_city(self):
        test_user = VKUser(test_id)
        assert test_user.find_city() == {'id' : 2, 'title' : 'Санкт-Петербург'}

    def test_search_people_by_users_search(self):
        search_dict = {
                'sex' : 1,
                'status' : 6,
                'age_from' : 25,
                'age_to' : 30,
                'city' : 1
            }
        test_user = VKUser(test_id, search=search_dict)
        assert test_user.search_people_by_users_search()['response']['count'] == 10

    def test_get_person_url(self):
        test_user = VKUser(test_id)
        assert test_user.get_person_url('23890940') == f'https://vk.com/id23890940'

    def test_get_top_photo(self):
        test_user = VKUser(test_id)
        photos = test_user.get_top_photo(test_user.user_id)
        assert len(photos) == 3
        for el in photos:
            assert el['user_id'] == test_user.user_id

    def test_search_cities(self):
        test_user = VKUser(test_id)
        assert test_user.search_cities({'q' : 'Санкт-Петербург'}) == {'response': {'count': 1, 'items': [{'id': 2, 'title': 'Санкт-Петербург'}]}}
class TestVkBot:
    def setup(self):
        print("method setup")   
    def teardown(self):
        print("method teardown") 

    def test_find_citi_in_VK(self):
        test_vk_bot = VkBot(test_id)
        assert test_vk_bot.find_citi_in_VK(test_id, 'неизвестный город') == False
        cities = test_vk_bot.find_citi_in_VK(test_id, 'Мурмаши')
        assert len(cities) == 2

    def test_opposite_sex(self):
        test_vk_bot = VkBot(test_id)
        assert test_vk_bot.opposite_sex() == '1'
        test_vk_bot = VkBot(test_id_female)
        assert test_vk_bot.opposite_sex() == '2'

    def test_get_user_sex(self):
        test_vk_bot = VkBot(test_id)
        assert test_vk_bot.get_user_sex() == 2

    def test_get_user_name_from_vk_id(self):
        test_vk_bot = VkBot(test_id)
        assert test_vk_bot._get_user_name_from_vk_id(test_id) == ['Димка', 'Хмелев', '|', 'ВКонтакте']

    def test_return_standard_values(self):
        test_vk_bot = VkBot(test_id)
        test_vk_bot.return_standard_values()
        assert test_vk_bot.answers == {'marital_status' : [], 'correction' : False}
        assert test_vk_bot.person_count == 0
        assert test_vk_bot.person_photos == ''
        assert test_vk_bot.result == {'response': {'count': 0, 'items' : []}}
        assert test_vk_bot.count == 0
        assert test_vk_bot.function_variable == 0

    def test_write_answer(self):
        test_vk_bot = VkBot(test_id)
        test_vk_bot.write_answer('НЕ ЖЕНАТ' ,'marital_status')
        assert ['НЕ ЖЕНАТ'] == test_vk_bot.answers['marital_status']
        test_vk_bot.write_answer(1 ,'person_count')
        assert 1 == test_vk_bot.answers['person_count']

    def test_convert_status(self):
        test_vk_bot = VkBot(test_id)
        test_vk_bot.write_answer('НЕ ЖЕНАТ' ,'marital_status')
        assert test_vk_bot.convert_status() == ['1']
    
    def test_search_people(self):
        search_dict = {
                'sex' : 1,
                'status' : 1,
                'age_from' : 18,
                'age_to' : 19,
                'city' : 2
            }
        test_vk_bot = VkBot(test_id)
        assert test_vk_bot.search_people(search_dict)['response']['count'] == 10

    def test_new_message_exception(self):
        test_vk_bot = VkBot(test_id)
        assert test_vk_bot.new_message_exception() == f"Я бот.Я не понял твоего ответа. Пожалуйста, ответь на вопрос."

    def test_create_keyboard(self):
        test_vk_bot = VkBot(test_id)
        assert test_vk_bot.create_keyboard() == VkKeyboard.get_empty_keyboard()
        test_keyboard = VkKeyboard(one_time=True)
        test_keyboard.add_button('Конпка 1', VkKeyboardColor.POSITIVE)
        test_keyboard.add_button('Конпка 2', VkKeyboardColor.NEGATIVE)
        test_keyboard.add_line()
        test_keyboard.add_button('Конпка 3', VkKeyboardColor.PRIMARY)
        test_keyboard.add_button('Конпка 4', VkKeyboardColor.SECONDARY)
        assert test_vk_bot.create_keyboard([['Конпка 1', 'POSITIVE'], ['Конпка 2', 'NEGATIVE'], ['Конпка 3', 'PRIMARY'], ['Конпка 4', 'SECONDARY']]) == test_keyboard.get_keyboard()

    def test_show_matched_pair(self):
        test_vk_bot = VkBot(test_id)
        search_dict = {
                'sex' : 1,
                'status' : 1,
                'age_from' : 18,
                'age_to' : 19,
                'city' : 2
            }
        test_vk_bot.control_questions = 100
        test_vk_bot.result = test_vk_bot.search_people(search_dict)
        test_vk_bot.show_matched_pair('Привет')
        assert test_vk_bot.control_questions == 101
        assert test_vk_bot.person_count == 1
        assert test_vk_bot.answers['person_1'] == 'ПРИВЕТ'

        result = test_vk_bot.show_matched_pair('Пока')
        assert result['bot_answer'] == 'Женя Солнцева \n https://vk.com/id447510679' # Тут проблема. Не уверен, что именно этот человек появится в следующий раз
        assert result['person_photos'] == 'photo447510679_456242691,photo447510679_456243473,photo447510679_456243677,' 
        
        test_keyboard = VkKeyboard(one_time=True)
        test_keyboard.add_button('Далее', VkKeyboardColor.POSITIVE)     
        assert result['keyboard'] == test_keyboard.get_keyboard()
        
        test_vk_bot.person_count = 9
        result = test_vk_bot.show_matched_pair('Проверка клавиатуры')
        test_keyboard = VkKeyboard(one_time=True)
        test_keyboard.add_button('Посмотреть следующие 10 вариантов', VkKeyboardColor.POSITIVE)
        test_keyboard.add_button('Начать поиск заново', VkKeyboardColor.NEGATIVE)
        assert result['keyboard'] == test_keyboard.get_keyboard()

    def test_get_removable_urls(self):
        search_dict = {
                'sex' : 1,
                'status' : 1,
                'age_from' : 18,
                'age_to' : 19,
                'city' : 2
            }
        test_vk_bot = VkBot(test_id)
        test_vk_bot.result = test_vk_bot.search_people(search_dict)
        test_vk_bot.get_removable_urls()
        assert len(test_vk_bot.removable_urls) == 10
    
    def test_add_table_to_bd(self):
        test_vk_bot = VkBot(test_id)
        assert test_vk_bot.add_table_to_bd() == True
        test_vk_bot.count_create_bd = 1
        assert test_vk_bot.add_table_to_bd() == False

    def test_find_user_in_bd(self):
        test_vk_bot = VkBot(test_id)
        Session = sessionmaker(bind=engine)
        session = Session()
        assert test_vk_bot.find_user_in_bd(session, User) == 1
        