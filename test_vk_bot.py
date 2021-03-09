from functions import create_text_keyboard, add_next_button, age_verification, checking_number_in_str

class TestVKBot:
    def setup(self):
        print("method setup")   
    def teardown(self):
        print("method teardown")  
    def test_create_text_keyboard(self):
        # 4 кнопки
        test_label_list = ['TEST_1', 'TEST_2', 'TEST_3', 'TEST_4']
        assert create_text_keyboard(test_label_list) == [[{"action":{"type":"text",
                                                                    "label":"TEST_1"}
                                                        },
                                                        {"action":{"type":"text",
                                                                    "label":"TEST_2"}
                                                        },
                                                        {"action":{"type":"text",
                                                                    "label":"TEST_3"}
                                                        },
                                                        {"action":{"type":"text",
                                                                    "label":"TEST_4"}
                                                        }]]
        # 5 кнопок
        test_label_list = ['TEST_1', 'TEST_2', 'TEST_3', 'TEST_4', 'TEST_5']
        assert create_text_keyboard(test_label_list) == [[{"action":{"type":"text",
                                                                    "label":"TEST_1"}
                                                        },
                                                        {"action":{"type":"text",
                                                                    "label":"TEST_2"}
                                                        },
                                                        {"action":{"type":"text",
                                                                    "label":"TEST_3"}
                                                        },
                                                        {"action":{"type":"text",
                                                                    "label":"TEST_4"}
                                                        }],
                                                        [{"action":{"type":"text",
                                                                    "label":"TEST_5"}
                                                        },
                                                        ]]
        # 7 кнопок
        test_label_list = ['TEST_1', 'TEST_2', 'TEST_3', 'TEST_4', 'TEST_5', 'TEST_6', 'TEST_7']
        assert create_text_keyboard(test_label_list) == [[{"action":{"type":"text",
                                                                    "label":"TEST_1"}
                                                        },
                                                        {"action":{"type":"text",
                                                                    "label":"TEST_2"}
                                                        },
                                                        {"action":{"type":"text",
                                                                    "label":"TEST_3"}
                                                        },
                                                        {"action":{"type":"text",
                                                                    "label":"TEST_4"}
                                                        }],
                                                        [{"action":{"type":"text",
                                                                    "label":"TEST_5"}
                                                        },
                                                        {"action":{"type":"text",
                                                                    "label":"TEST_6"}
                                                        },
                                                        {"action":{"type":"text",
                                                                    "label":"TEST_7"}
                                                        },
                                                        ]]
        # 9 кнопок
        test_label_list = ['TEST_1', 'TEST_2', 'TEST_3', 'TEST_4', 'TEST_5', 'TEST_6', 'TEST_7', 'TEST_8', 'TEST_9']
        assert create_text_keyboard(test_label_list) == [[{"action":{"type":"text",
                                                                    "label":"TEST_1"}
                                                        },
                                                        {"action":{"type":"text",
                                                                    "label":"TEST_2"}
                                                        },
                                                        {"action":{"type":"text",
                                                                    "label":"TEST_3"}
                                                        },
                                                        {"action":{"type":"text",
                                                                    "label":"TEST_4"}
                                                        }],
                                                        [{"action":{"type":"text",
                                                                    "label":"TEST_5"}
                                                        },
                                                        {"action":{"type":"text",
                                                                    "label":"TEST_6"}
                                                        },
                                                        {"action":{"type":"text",
                                                                    "label":"TEST_7"}
                                                        },
                                                        {"action":{"type":"text",
                                                                    "label":"TEST_8"}
                                                        },
                                                        ],
                                                        [
                                                        {"action":{"type":"text",
                                                                    "label":"TEST_9"}
                                                        },
                                                        ]]

    def test_add_next_button(self):
        test_label_list = ['TEST_1', 'TEST_2', 'TEST_3', 'TEST_4']
        result = add_next_button(create_text_keyboard(test_label_list))
        assert result == [[{"action":{"type":"text",
                                    "label":"TEST_1"}
                            },
                            {"action":{"type":"text",
                                        "label":"TEST_2"}
                            },
                            {"action":{"type":"text",
                                        "label":"TEST_3"}
                            },
                            {"action":{"type":"text",
                                        "label":"TEST_4"}
                            }],
                            [{"action":{"type":"text",
                                        "label":"Далее"}
                            }
                            ]]

    def test_age_verification(self):
        # Проверка минимального возраста
        # Верный возраст
        assert age_verification({'min_age' : 18}) == True
        # Неверный возраст
        assert age_verification({'min_age' : -10}) == False
        # Проверка максимального возраста
        # Верный возраст
        assert age_verification({'max_age' : 25}, min_age=18) == True
        # Неверный возраст
        assert age_verification({'max_age' : 25}, min_age=35) == False

    def test_checking_number_in_str(self):
        # Проверка на положительное число
        assert checking_number_in_str('250') == True
        # Проверка на отрицательно число
        assert checking_number_in_str('-167') == True
        # Проверка слово
        assert checking_number_in_str('слово') == False
        # Проверка слово c '-'
        assert checking_number_in_str('-не слово') == False