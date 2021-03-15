from token_data import user_access_token
from classes import VKUser

class TestVKUser:
    def __init__(self):
        self.test_id = '23890940'
    def setup(self):
        print("method setup")   
    def teardown(self):
        print("method teardown") 


    def test_find_sex(self):
        test_user = VKUser(self.test_id)
        assert test_user.find_sex() == '2'
