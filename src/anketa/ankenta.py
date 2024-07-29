# ankenta.py

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
        self.message_counter = 0                                            # Счётчик сообщений
        self.related_table:str = setting_dict['related_table']              # Связанная таблица (для получения информации с других таблиц)
        
    # Отправка соообщений    
    def __send_some_message(self, id, some_text, keyboard=None) -> None:
    
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
        
    # Проверка на наличии анкеты
    def check_anketa(self,  table_name:str, vk_user_id) -> None:
        
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
    def get_anketa_info(self, vk_user_id:str,) -> None:
        
        connect = sqlite3.connect(self.db.db_name+".db")
        cursor = connect.cursor()
        
        __SELECT_text = f'SELECT * FROM {self.table_name} WHERE user_id LIKE (?)'
        
        anketa_info = list(cursor.execute(__SELECT_text, (vk_user_id,)).fetchall()[0])
        
        #print(f'{anketa_info=}')
        
        anketa_message = ''
        
        for index in range(2, len(anketa_info)):
            anketa_message_line = f'|{anketa_info[index].capitalize()}\n\n'        
            anketa_message += anketa_message_line
        self.__send_some_message(id=vk_user_id, some_text=anketa_message)
        
        anketa_menu = VkKeyboard(one_time=True)
        anketa_menu.add_button(label='Заполнить анкету заново')
        anketa_menu.add_line()
        anketa_menu.add_button(label="Вернуться в меню поиска",color=VkKeyboardColor.NEGATIVE)    
        
        self.__send_some_message(id=vk_user_id, some_text="\n______________\n|Выберите что будем делать дальше:", keyboard=anketa_menu)
        
    # Обновления значений в БД
    def update_anceta_column(self, vk_user_id:str, column_name:str=None, column_meaning:str="") -> None:
        connect = sqlite3.connect(self.db.db_name+".db")
        cursor = connect.cursor()
        
        UPDATE_text = f'UPDATE {self.table_name} SET {column_name} = ? WHERE user_id = ?'
        cursor.execute(UPDATE_text, (column_meaning, vk_user_id))
        
        connect.commit()
        connect.close()
        pass
    
    # Регистрация пользователя 
    def register_user(self, vk_user_id) -> None:
        
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
    def create_anketa(self, vk_user_id, msg) -> None:
        
        instruction = self.instruction
        key_word_list = list(self.instruction.keys())
        key_word_counter = len(key_word_list)
        message_instruction = self.message_instruction
        next_button = VkKeyboard(one_time=True)
        next_button.add_button(label='Далее')
        
        if self.counter == key_word_counter:
            print("Обнулили")
            self.message_counter = 0
            self.kw = 'anketa_menu'
        
        if (msg == 'далее') or (msg =='хорошо, создадим анкету'):
            self.__send_some_message(id=vk_user_id, some_text=message_instruction[key_word_list[self.counter]])
            self.counter +=1
        
        else:
            self.update_anceta_column(vk_user_id=vk_user_id, 
                                          column_name=instruction[key_word_list[self.counter-1]],
                                          column_meaning=msg)
            
            self.__send_some_message(id=vk_user_id, some_text="После ввода информации, нажмите далее", keyboard=next_button)
            
        if  key_word_counter*2 == self.message_counter:
            print("Обнулили")
            self.message_counter = 0
            self.kw = 'anketa_menu'
    
    # Заполнение анкеты заново
    def update_anketa(self, vk_user_id, msg) -> None:
        
        instruction = self.instruction
        key_word_list = list(self.instruction.keys())
        key_word_counter = len(key_word_list)
        message_instruction = self.message_instruction
        next_button = VkKeyboard(one_time=True)
        next_button.add_button(label='Далее')
        
        if self.counter == key_word_counter:
            print("Обнулили")
            self.message_counter = 0
            self.kw = 'anketa_menu'
        
        if (msg == 'далее') or (msg =='заполнить анкету заново'):
            self.__send_some_message(id=vk_user_id, some_text=message_instruction[key_word_list[self.counter]])
            self.counter +=1
        
        else:
            self.update_anceta_column(vk_user_id=vk_user_id, 
                                          column_name=instruction[key_word_list[self.counter-1]],
                                          column_meaning=msg)
            
            self.__send_some_message(id=vk_user_id, some_text="После ввода информации, нажмите далее", keyboard=next_button)
            
        if  key_word_counter*2 == self.message_counter:
            print("Обнулили")
            self.message_counter = 0
            self.kw = 'anketa_menu'
                 
    # Редактирование анкеты
    def edit_anketa(self,) -> None:
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
        
        try:
            connect = sqlite3.connect(self.db.db_name+".db")
            cursor = connect.cursor()

            link = list(cursor.execute(f"SELECT * FROM Links").fetchall())[0][2]

            message = f"Если вы хотите написать отзыв о нашем боте, то перейдите по ссылке:\n{link}"
            self.__send_some_message(id=vk_user_id, some_text=message)
        
        except IndexError:
            message = f"Ссылки пока что нет"
            self.__send_some_message(id=vk_user_id, some_text=message)
    
    # Поиски анкет                
    def start_find(self, vk_user_id) -> None:
        
        table_name = self.related_table
        
        if table_name is None:
            pass
        
        connect = sqlite3.connect(self.db.db_name+".db")
        cursor = connect.cursor()
        
        print(table_name,"<<<<<<<")
        
        __TEXT = f'SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT 1;'
        
        random_anketa = list(cursor.execute(__TEXT).fetchall()[0])
        
        
        anketa_info = ""
        
        for index in range(2, len(random_anketa)):
            anketa_info += f'{str(random_anketa[index]).capitalize()}\n'
        
        
        find_keyboard = VkKeyboard(one_time=True)
        find_keyboard.add_button("👍")
        find_keyboard.add_button("👎")
        find_keyboard.add_line()
        find_keyboard.add_button("Вернуться в меню поиска", color=VkKeyboardColor.NEGATIVE)
        
        self.__send_some_message(id=vk_user_id, some_text=anketa_info, keyboard=find_keyboard)
                
        print(random_anketa)
    
    # Отправка отклика
    def post_callback(self, vk_user_id) -> None:
        pass
    
    # Просмотр откликов    
    def get_callback(self, vk_user_id) -> None:
        pass
                
    # Тело класса анкеты         
    def main(self, msg:str, vk_user_id:str) -> None:
    
        # Проверка на наличие анкеты
        if self.kw == 'anketa_check':
            self.check_anketa(table_name=self.table_name, vk_user_id=vk_user_id)
            
        # Регистрация пользователя    
        if (msg == 'хорошо, создадим анкету') and (self.kw == 'anketa_check'):
            print(1)
            self.register_user(vk_user_id=vk_user_id)
            
            self.kw = 'create_anketa'
        
        # Создание анкеты   
        if (self.kw == 'create_anketa'):
            #print("Отрабатываем")
            self.create_anketa(vk_user_id=vk_user_id, msg=msg)
        
        # Поиск 
        if msg == "поиск" or msg =='👎':
            self.kw = "find_anketa"
            
        if (self.kw == "find_anketa") :
            self.start_find(vk_user_id=vk_user_id)
        
        # Отправка обратной связи о боте
        if msg == 'написать отзыв о боте':
            self.get_callback_link(vk_user_id)
            self.kw = "anketa_menu"
       
        # Получение информации об анкете
        if msg == 'моя анкета':
            self.kw = 'anketa_info'
            #print("Проверка анкеты")
            self.get_anketa_info(vk_user_id=vk_user_id)
        
        # Редактирование анкеты
        if msg == 'заполнить анкету заново' or self.kw =='update_anketa':
            self.kw = 'update_anketa'
            self.update_anketa(vk_user_id=vk_user_id, msg=msg)
        
        # Основное меню анкеты
        if (self.kw == 'anketa_menu') or (msg == "/anketa_menu") or (msg =="вернуться в меню поиска"):
            self.get_anketa_menu(vk_user_id)
            self.kw = "anketa_menu"