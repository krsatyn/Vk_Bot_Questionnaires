# ankenta.py
# main.py

import sqlite3
import vk_api as vk

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType


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
        self.kw:str = "anketa_check"                                        # Ключевое слово    
        self.counter:int = 0                                                # Счетчик включений ключевого слова инструкций
        self.message_instruction:dict = setting_dict['message_instruction'] # Сообщения для пользователя 
        self.message_counter = 0
        
    # Отправка соообщений    
    def __send_some_message(self, id, some_text, keyboard=None):
    
        post = {
            "user_id":id, 
            "message":some_text, 
            "random_id":0,}

        if keyboard != None:
            post['keyboard'] = keyboard.get_keyboard() 

        self.vk_session.method("messages.send", post)    
    
    # Меню просмотра СВОей анкеты
    def anketa_check_menu(self,)->None:
        anketa_menu = VkKeyboard(one_time=True)
        anketa_menu.add_button(label='Редактировать анкету')
        anketa_menu.add_line()
        anketa_menu.add_button(label="вернуться в меню поиска",color=VkKeyboardColor.NEGATIVE)
    
    # Меню редактирования анкеты
    def edit_anketa_info() -> None:
        
        # Получить всю информацию об анкете 
        anketa_info = []
        # Генератор кнопок
        max_column = len(anketa_info[2:])
        
        for button_number in range(max_column):
            # тут генерим кнопки для редактирования
            pass
        anketa_menu = VkKeyboard(one_time=True)
        anketa_menu.add_button(label='Редактировать анкету')
        anketa_menu.add_line()
        anketa_menu.add_button(label="вернуться в меню поиска",color=VkKeyboardColor.NEGATIVE)    
             
    # Проверка на наличии анкеты
    def check_anketa(self,  table_name:str, vk_user_id):
        
        check_anketa_keyboard = VkKeyboard(one_time=1)
        check_anketa_keyboard.add_button(label="Заполнить анкету", color=VkKeyboardColor.POSITIVE)
        check_anketa_keyboard.add_line()
        check_anketa_keyboard.add_button(label="Вернуться в меню поиска", color=VkKeyboardColor.NEGATIVE)
        
        connect = sqlite3.connect(self.db.db_name+".db")
        cursor = connect.cursor()

        __SELECT_text = f'SELECT * FROM {table_name} WHERE user_id LIKE (?)'
        
        user_id_check = cursor.execute(__SELECT_text, (vk_user_id,)).fetchall()
        
        #print(user_id_check)
        #print(f"{len(list(user_id_check))}")
        
        if len(user_id_check) == 0:
                        
            confirmation_keyboard = VkKeyboard(one_time=True)
            confirmation_keyboard.add_button(label="Хорошо, создадим анкету", color=VkKeyboardColor.POSITIVE)
            confirmation_keyboard.add_line()
            confirmation_keyboard.add_button(label="Назад в меню", color=VkKeyboardColor.NEGATIVE)
            
            self.__send_some_message(id=vk_user_id, some_text="У вас еще нет анкеты. Давайте заполним её", keyboard=confirmation_keyboard)

        else:
            self.kw = 'anketa_menu'
            
    # Получить всю информацию об анкете
    def get_anketa_info(self, vk_user_id:str,):
        
        connect = sqlite3.connect(self.db.db_name+".db")
        cursor = connect.cursor()
        
        anketa_info = ''
        
        anketa_message = f"{anketa_info[2]}\n{anketa_info[3]}\n{anketa_info[4]}"
        self.__send_some_message(id=vk_user_id, some_text="")
      
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
    
    # Регистрация пользователя 
    def register_user(self, vk_user_id):
        
        table_name = self.table_name
        
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
    
    # Создание анкеты пользователя
    def create_anketa(self, vk_user_id, msg):
        
        #клавиа
        
        # Получение параметров анкеты
        instruction = self.instruction
        #print("словарь инструкций",instruction)
        
        key_word_list = list(self.instruction.keys())
        key_word_counter = len(key_word_list)
        
        message_instruction = self.message_instruction
        
        next_button = VkKeyboard(one_time=True)
        next_button.add_button(label='Далее')        
        #print(self.message_counter)
        
        try:
            if self.message_counter % 2 == 0:
                print("Мы отправляем")
                self.__send_some_message(id=vk_user_id, some_text=message_instruction[key_word_list[self.message_counter]])
                self.message_counter +=1

                print(self.message_counter)

            else:
                print("Мы слушаем")
                self.update_anceta_column(vk_user_id=vk_user_id, 
                                          column_name=instruction[key_word_list[self.message_counter-1]],
                                          column_meaning=msg)
                self.message_counter +=1
                print(self.message_counter)

            if key_word_counter*2 == self.message_counter:
                print("Обнулили")
                self.message_counter = 0
                self.kw = 'anketa_menu'
        
        except IndexError:
                print("Обнулили")
                self.message_counter = 0
                self.kw = 'anketa_menu'
                
    # Редактирование анкеты
    def edit_anketa(self,):
        pass
    
    # Основное меню анкеты
    def get_anketa_menu(self,vk_user_id)-> None:
        
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
        
        self.__send_some_message(vk_user_id, "Ты в меню", menu_keyboard)
        
    
    # Просмотр ответов на анкету
    def response_anketa(self,)-> None:
        pass
    
    # Ссылка на обратную связь
    def get_callback_link(self, vk_user_id) -> None:
        
        connect = sqlite3.connect(self.db.db_name+".db")
        cursor = connect.cursor()
        
        link = list(cursor.execute(f"SELECT * FROM Links").fetchall())[0][2]
        
        message = f"Если вы хотите написать отзыв о нашем боте, то перейдите по ссылке:\n{link}"
        self.__send_some_message(id=vk_user_id, some_text=message)
            
            
    def main(self, msg:str, vk_user_id:str):
        
        #print(msg)
        #print(f"{self.kw=}")
        
        # Проверка на наличие анкеты
        if self.kw == 'anketa_check':
            self.check_anketa(table_name=self.table_name, vk_user_id=vk_user_id)
        
        # Создание анкеты    
        if (msg == 'хорошо, создадим анкету') and (self.kw == 'anketa_check'):
            self.register_user(vk_user_id=vk_user_id)
            self.kw = 'create_anketa'
            
        if (self.kw == 'create_anketa'):
            #print("Отрабатываем")
            self.create_anketa(vk_user_id=vk_user_id, msg=msg)
        
        if msg == 'написать отзыв о боте':
            self.get_callback_link(vk_user_id)
            self.kw = "anketa_menu"
       
        if msg == 'моя анкета':
            self.kw = 'anketa_info'
            #print("Проверка анкеты")
            self.get_anketa_info(vk_user_id=vk_user_id)
            
        if (self.kw == 'anketa_menu') or (msg == "/anketa_menu") or (msg =="вернуться в меню поиска"):
            self.get_anketa_menu(vk_user_id)
            
        #('kw',self.kw)