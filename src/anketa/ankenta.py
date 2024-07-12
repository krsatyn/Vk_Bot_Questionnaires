# ankenta.py
# main.py

import sqlite3
import vk_api as vk

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from numpy import random

class AnketaConstruct():
    
    def __init__(self, 
                 vk_session,
                 session_api,
                 longpool,
                 setting_dict:dict,):
        
        self.vk_session = vk_session                                        # Вк сессия
        self.session_api = session_api                                      # Aпи для сессии 
        self.longpool =  longpool                                           # Очередь
        self.db = setting_dict['db']                                        # подключение базы данных
        self.table_name:str = setting_dict['table_name']                    # Имя таблицы
        self.create_kw:str = setting_dict['create_kw']                      # Стартовое слово для создания анкеты
        self.instruction:dict = setting_dict['instruction']                 # Набор инструкций {что делаем:куда делаем}                                 
        self.kw:str = ""                                                    # Ключевое слово    
        self.counter:int = 0                                                # Счетчик включений ключевого слова инструкций
        self.message_instruction:dict = setting_dict['message_instruction'] # Сообщения для пользователя 
        
    # Отправка соообщений    
    def __send_some_message(self, id, some_text, keyboard=None):
    
        post = {
            "user_id":id, 
            "message":some_text, 
            "random_id":0,}

        if keyboard != None:
            post['keyboard'] = keyboard.get_keyboard() 

        self.vk_session.method("messages.send", post)    
    
    # Создание анкет
    def create_anketa(self, table_name:str, vk_user_id):
        
        connect = sqlite3.connect(self.db.db_name+".db")
        cursor = connect.cursor()

        __SELECT_text = f'SELECT * FROM {table_name} WHERE user_id LIKE (?)'
        
        user_id_check = cursor.execute(__SELECT_text, (vk_user_id,)) 
        if len(user_id_check.fetchall()) > 0:
            return 0
        
        __INSERT_text = f'INSERT INTO {table_name} (user_id) VALUES (?)'
        cursor.execute(__INSERT_text, (vk_user_id,))
        connect.commit()
        connect.close()  
    
    # Проверка на наличии анкеты
    def check_anketa(self,  table_name:str, vk_user_id):
        
        check_anketa_keyboard = VkKeyboard(one_time=1)
        check_anketa_keyboard.add_button(label="Заполнить анкету", color=VkKeyboardColor.POSITIVE)
        check_anketa_keyboard.add_line()
        check_anketa_keyboard.add_button(label="Вернуться в меню поиска", color=VkKeyboardColor.NEGATIVE)
        connect = sqlite3.connect(self.db.db_name+".db")
        cursor = connect.cursor()

        __SELECT_text = f'SELECT * FROM {table_name} WHERE user_id LIKE (?)'
        
        user_id_check = cursor.execute(__SELECT_text, (vk_user_id,)) 
        if len(user_id_check.fetchall()) > 0:
            #получение данных об анкете
            self.get_anketa_info(self,)    
        else:
            self.__send_some_message(id=vk_user_id, some_text="У вас еще нет анкеты. Давайте заполним её")
            
            
    # Получить всю информацию об анкете
    def get_anketa_info(self,):
        pass    
    
    # Поиск других анкет
    def find_another_anketa(self, id_vk_user:str):
        connect = sqlite3.connect(self.db.db_name+".db")
        cursor = connect.cursor()
        
        cursor.execute('',())
        
        
        random_user = random.randint()
        
        self.__send_some_message(id=id_vk_user, )
    
    # Обновления значений в БД
    def update_anceta_column(self, vk_user_id:str, column_name:str=None, column_meaning:str=""):
        connect = sqlite3.connect(self.db.db_name+".db")
        cursor = connect.cursor()
        
        UPDATE_text = f'UPDATE {self.table_name} SET {column_name} = ? WHERE user_id = ?'
        cursor.execute(UPDATE_text, (column_meaning, vk_user_id))
        
        connect.commit()
        connect.close()
    
    # Начало поиска анкет                
    def start_find(self,):
        pass
    
    # Конец поиска анкет
    def cancel_find(self,):
        pass
    
    # Редактирование анкеты
    def edit_anketa(self,):
        pass
    
    # Основное меню анкеты
    def get_anketa_menu(self,vk_user_id):
        menu_keyboard = VkKeyboard(one_time=True)
        menu_keyboard.add_button(label="Поиск", color=VkKeyboardColor.POSITIVE)
        menu_keyboard.add_line()
        menu_keyboard.add_button(label="Отклики",)
        menu_keyboard.add_line()
        menu_keyboard.add_button(label="Моя анкета",)
        menu_keyboard.add_line()
        menu_keyboard.add_button(label="Написать отзыв о боте",)
        menu_keyboard.add_line()
        menu_keyboard.add_button(label="Назад в меню", color=VkKeyboardColor.NEGATIVE)
        
        self.__send_some_message(vk_user_id, "Ты в меню анкеты", menu_keyboard)
    
    # Просмотр ответов на анкету
    def response_anketa(self,):
        pass
    
    def main(self, msg:str, vk_user_id:str):
        
        instruction = self.instruction
        key_word_list = list(instruction.keys())
        key_word_counter = len(key_word_list)
        
        print(f"{self.kw=}")
        
        if key_word_counter == self.counter:
            self.kw = "" 
        
        # Запись значений в бд согласно инструкции
        if (key_word_list.count(self.kw) !=0 ) and (instruction.get(self.kw) is not None) and (self.kw != 'start'):
            
            try:
                # print("мы в круге: ", instruction.get(self.kw))
                self.update_anceta_column(vk_user_id=vk_user_id, column_name=instruction.get(self.kw), column_meaning=msg)
                self.counter += 1
                self.kw = key_word_list[self.counter]
                self.__send_some_message(vk_user_id, some_text= self.message_instruction[key_word_list[self.counter]])
            
            except (KeyError, IndexError):
                print("kw обнулён")
                self.kw = 'anketa_menu'
                
        # Запись первого сообщения
        if (self.kw == "start") and (instruction.get(self.kw) is not None):
            
            self.update_anceta_column(vk_user_id=vk_user_id, column_name=instruction.get(self.kw), column_meaning=msg)
            
            try:
                self.counter += 1
                self.kw = key_word_list[self.counter]
                self.__send_some_message(vk_user_id, some_text= self.message_instruction[key_word_list[self.counter]])
                print(f'Из словаря {key_word_list=}\nMы выбрали влюч {key_word_list[self.counter]=}')
                
            except (KeyError, IndexError):
                print("мы в ошибке")
                print(">>>", self.kw)
                self.kw = 'anketa_menu'
                self.__send_some_message(vk_user_id, some_text='Анкета заполена)')
                return 0
        
        # Начало работы  
        if msg == self.create_kw:
            
            self.create_anketa(table_name=self.table_name,vk_user_id=vk_user_id)
            self.__send_some_message(vk_user_id, some_text= self.message_instruction["start"])
            self.kw = "start"
        
        if msg == 'моя анкета':
            ''
        
        # Поиск анкет
        if msg == 'поиск':
            self.find_another_anketa()
            
        
        if (self.kw == 'anketa_menu') or (msg == "/anketa_menu") or ("Вернуться в меню поиска"):
            self.get_anketa_menu(vk_user_id)
            
        