# ankenta.py
# main.py

import sqlite3
import vk_api as vk

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType

from database_func import DataBase


class AnketaConstruct():
    
    def __init__(self,
                 vk_session,
                 longpool,
                 session_api,
                 db:DataBase,
                 table_name:str,
                 create_kw:str="",
                 instruction:dict ={"first_qestion":"first_qestion"}) -> None:
        
        self.vk_session = vk_session                                    # Вк сессия
        self.session_api = session_api                                  # Aпи для сессии 
        self.longpool =  longpool                                       # Очередь
        self.db = db                                                    # подключение базы данных
        self.table_name = table_name                                    # Имя таблицы
        self.create_kw = create_kw                                      # Стартовое слово для создания анкеты
        self.instruction = instruction                                  # Набор инструкций {что делаем:куда делаем}                                 
        self.kw = ""                                                    # Ключевое слово    
        
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
    
    # Обновления значений в БД
    def update_anceta_column(self, vk_user_id:str, column_name:str=None, column_meaning:str=""):
        connect = sqlite3.connect(self.db.db_name+".db")
        cursor = connect.cursor()
        
        UPDATE_text = f'UPDATE {self.table_name} SET {column_name} = ? WHERE user_id = ?'
        cursor.execute(UPDATE_text, (column_meaning, vk_user_id))
        
        connect.commit()
        connect.close()
                    
    def start_find(self,):
        pass
    
    def cancel_find(self,):
        pass
    
    def edit_anketa(self,):
        pass
    
    def response_anketa(self,):
        pass
    
    def send_callback(self,):
        pass
    
    def main(self, msg:str, vk_user_id:str):
        instruction = self.instruction
        
        print(f"{self.kw=}")
        
        # Запись первого сообщения
        if (self.kw == "start") and (instruction.get(self.kw) is not None):
            
            print("записываем имя")
            
            self.update_anceta_column(vk_user_id=vk_user_id, column_name=instruction.get(self.kw), column_meaning=msg)
            self.__send_some_message(vk_user_id, some_text="оп оп, обработали запросик по словарику")
            self.kw=''
        
        #print(instruction.get(list(instruction.keys())[0]))
           
        # Начало работы        
        if msg == self.create_kw:
            
            self.create_anketa(table_name=self.table_name,vk_user_id=vk_user_id)
            self.__send_some_message(vk_user_id, some_text="Напиши о друге")
            self.kw = "start"
        