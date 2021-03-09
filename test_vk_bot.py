from functions import create_text_keyboard, add_next_button

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