# database_func.py

import sqlite3

class DataBase():
    
    def __init__(self, db_name:str="db") -> None:
        self.db_name = db_name
    
    # Создаем бд
    def create_database(self, name_database:str) -> None:

        try:
            self.connect = sqlite3.connect(name_database+".db")
            print(f"\n>Успешно, создана база данных с именем {name_database}.db")

        except (TypeError,SyntaxError):
            print(f">ОШИБКА СОЗДАНИЕ СОЗДАНИЕ БАЗЫ ДАННЫХ С ИМЕНЕМ {name_database}.db")
            print(f"->Проверьте формат имени, необходимо что бы был формат <str>")
            print(f"->Текущий тип: {type(name_database)}")

        return 0

    # Создание таблицы для анкеты пользователя
    def create_users_form_table(self,) -> None:
        '''Создание таблицы
        |id:int key|user_id:str|name:str|city:str|age:int|
        '''
        
        cursor = self.connect.cursor()
        
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS UsersForm (
            id INTEGER PRIMARY KEY,
            user_id TEXT ,
            name TEXT ,
            city TEXT ,
            age INTEGER
            )                            
            ''')

            self.connect.commit()
            print(">Таблица UsersForm успешно создана")
        
        except sqlite3.OperationalError:
            print("\n> Ошибка создания таблицы")
            print(f"->Имя таблицы |таблица для анкеты пользователя|")
            print(f"->Название таблицы UsersForm")

    # Создание таблицы для анкет проектов
    def create_projects_form_table(self,) -> None:
        '''Создание таблицы
        |id:int key|user_id:str|project_info:str|find_teams:str|
        '''
        
        cursor = self.connect.cursor()
        
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ProjectsForm (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            project_name TEXT,
            project_info TEXT,
            find_teams TEXT 
            )                            
            ''')

            self.connect.commit()
            print(">Таблица ProjectsForm успешно создана")
        
        except sqlite3.OperationalError:
            print("\n> Ошибка создания таблицы")
            print(f"->Имя таблицы |таблица для анкет проектов|")
            print(f"->Название таблицы ProjectsForm")
    
    # Таблица для лайкнувших проект
    def create_callback_projects_form_table(self,):
        '''Создание таблицы
        |id:int key|user_id:str|like_user_id:str|info:str|
        '''
        
        cursor = self.connect.cursor()
        
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS CallbackProjectsForm (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            like_user_id TEXT,
            like_user_name,
            user_info TEXT 
            )                            
            ''')

            self.connect.commit()
            print(">Таблица CallbackProjectsForm успешно создана")
        
        except sqlite3.OperationalError:
            print("\n> Ошибка создания таблицы")
            print(f"->Имя таблицы |таблица для лайков анкеты проектов|")
            print(f"->Название таблицы CallbackProjectsForm")
    
    # Таблица пользователя для поиска разработчика 
    def create_project_finder_from_table(self,) -> None:
        '''Создание таблицы
        |id:int key|user_id:str|name:str|user_info:str|
        '''
        
        cursor = self.connect.cursor()
        
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ProjectFinder(
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            user_name TEXT,
            user_info TEXT 
            )                            
            ''')

            self.connect.commit()
            print(">Таблица ProjectFinder успешно создана")
        
        except sqlite3.OperationalError:
            print("\n> Ошибка создания таблицы")
            print(f"->Имя таблицы |Таблица пользователя для поиска проектов|")
            print(f"->Название таблицы ProjectFinder")
    
    # Таблица для лайкнувших разработчика
    def create_callback_project_finder_from_table(self,):
        '''Создание таблицы
        |id:int key|user_id:str|project_info:str|find_teams:str|
        '''
        
        cursor = self.connect.cursor()
        
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS CallbackProjectsFinderForm (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            like_user_id TEXT,
            like_user_name TEXT,
            user_info TEXT 
            )                            
            ''')

            self.connect.commit()
            print(">Таблица CallbackProjectsFinderForm успешно создана")
        
        except sqlite3.OperationalError:
            print("\n> Ошибка создания таблицы")
            print(f"->Имя таблицы |таблица для лайков анкеты проектов|")
            print(f"->Название таблицы CallbackProjectsFinderForm")
    
    # Создание таблицы анкеты для поиска однофорумчан
    def create_one_formers_from_table(self,) -> None:
        '''Создание таблицы
        |id:int key|user_id:str|one_formers_info:str|
        '''
        
        cursor = self.connect.cursor()
        
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS OneFormers (
            id INTEGER PRIMARY KEY,
            user_id TEXT ,
            name TEXT,
            one_formers_info TEXT 
            )                            
            ''')

            self.connect.commit()
            print(">Таблица OneFormers успешно создана")
        
        except sqlite3.OperationalError:
            print("\n> Ошибка создания таблицы")
            print(f"->Имя таблицы |таблица для анкет проектов|")
            print(f"->Название таблицы one_formers")
        
    # Создание таблицы анкета наставника
    def create_mentors_profile_from_table(self,) -> None:
        '''Создание таблицы
        |id:int key|user_id:str|mentors_profile:str|
        '''
        
        cursor = self.connect.cursor()
        
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS MentorsProfile (
            id INTEGER PRIMARY KEY,
            user_id TEXT ,
            name TEXT,
            mentors_profile TEXT 
            )                            
            ''')

            self.connect.commit()
            print(">Таблица MentorsProfile успешно создана")

        except sqlite3.OperationalError:
            print("\n> Ошибка создания таблицы")
            print(f"->Имя таблицы |таблицы анкета наставника|")
            print(f"->Название таблицы mentors_profile")

    # Создание таблицы искателя наставника
    def create_mentors_finder_profile_from_table(self,) -> None:
        
        '''Создание таблицы
        |id:int key|user_id:str|name:str|user_info:str|
        '''
        
        cursor = self.connect.cursor()
        
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS MentorsFinder(
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            user_name TEXT,
            user_info TEXT 
            )                            
            ''')

            self.connect.commit()
            print(">Таблица MentorsFinder успешно создана")
        
        except sqlite3.OperationalError:
            print("\n> Ошибка создания таблицы")
            print(f"->Имя таблицы |Таблица пользователя для поиска Ментора|")
            print(f"->Название таблицы MentorsFinder")
        
    
    # Таблица для лайкнувших подаванов
    def create_callback_mentor_finder_from_table(self,):
        '''Создание таблицы
        |id:int key|user_id:str|project_info:str|find_teams:str|
        '''
        
        cursor = self.connect.cursor()
        
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS CallbackFinderMentorForm(
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            like_user_id TEXT,
            like_user_name TEXT,
            user_info TEXT 
            )                            
            ''')

            self.connect.commit()
            print(">Таблица CallbackFinderMentorForm успешно создана")

        except sqlite3.OperationalError:
            print("\n> Ошибка создания таблицы")
            print(f"->Имя таблицы |Таблица для лайкнувших подаванов|")
            print(f"->Название таблицы CallbackFinderMentorForm")
            
        
    # Таблица для лайкнувших Менторов
    def create_callback_mentor_from_table(self,):
        '''Создание таблицы
        |id:int key|user_id:str|project_info:str|find_teams:str|
        '''
        
        cursor = self.connect.cursor()
        
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS CallbackMentorForm(
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            like_user_id TEXT,
            like_user_name TEXT,
            user_info TEXT 
            )                            
            ''')

            self.connect.commit()
            print(">Таблица CallbackMentorForm успешно создана")

        except sqlite3.OperationalError:
            print("\n> Ошибка создания таблицы")
            print(f"->Имя таблицы |Таблица для лайкнувших Менторов|")
            print(f"->Название таблицы CallbackMentorForm")
            
    def create_callback_partner_offers_from_table(self,) -> None:
        '''Создание таблицы
        |id:int key|user_id:str|project_info:str|find_teams:str|
        '''
        
        cursor = self.connect.cursor()
        
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS CallbackOffersForm(
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            like_user_id TEXT,
            like_user_name TEXT,
            user_info TEXT 
            )                            
            ''')

            self.connect.commit()
            print(">Таблица CallbackOffersForm успешно создана")

        except sqlite3.OperationalError:
            print("\n> Ошибка создания таблицы")
            print(f"->Имя таблицы |Таблица для Предложений|")
            print(f"->Название таблицы CallbackOffersForm")
           
    # Создание таблицы  партнерские предложения
    def create_partner_offers_from_table(self,) -> None:
        '''Создание таблицы
        |id:int key|user_id:str|partner_offers:str|
        '''
        
        cursor = self.connect.cursor()
        
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS PartnerOffers (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            user_name TEXT,
            partner_offers TEXT 
            )                            
            ''')

            self.connect.commit()
            print(">Таблица PartnerOffers успешно создана")
        
        except sqlite3.OperationalError:
            print("\n> Ошибка создания таблицы")
            print(f"->Имя таблицы |партнерские предложения|")
            print(f"->Название таблицы PartnerOffers")
    
    # Создание таблицы заявок в друзья
    def create_callback_frends_from_table(self,):
        '''Создание таблицы
        |id:int key|user_id:str|project_info:str|find_teams:str|
        '''
        
        cursor = self.connect.cursor()
        
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS CallbackFrendsForm(
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            like_user_id TEXT,
            like_user_name TEXT,
            user_info TEXT 
            )                            
            ''')

            self.connect.commit()
            print(">Таблица CallbackFrendsForm успешно создана")

        except sqlite3.OperationalError:
            print("\n> Ошибка создания таблицы")
            print(f"->Имя таблицы |Таблица для лайкнувших друзей|")
            print(f"->Название таблицы CallbackFrendsForm")
            
    # Создание таблицы просто друзья
    def create_just_friends_from_table(self,) -> None:
        '''Создание таблицы
        |id:int key|user_id:str|just_friends_info:str|
        '''
        
        cursor = self.connect.cursor()
        
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS JustFriends (
            id INTEGER PRIMARY KEY,
            user_id            TEXT,
            user_name          TEXT,
            just_friends_info  TEXT 
            )                            
            ''')

            self.connect.commit()
            print(">Таблица JustFriends успешно создана")
        
        except sqlite3.OperationalError:
            print("\n> Ошибка создания таблицы")
            print(f"->Имя таблицы |просто друзья|")
            print(f"->Название таблицы JustFriends")
    
    # Создание таблицы ссылки
    def create_links_from_table(self,) -> None:
        '''Создание таблицы
        |id:int key|link:str|
        '''
        
        cursor = self.connect.cursor()
        
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Links (
            id INTEGER PRIMARY KEY,
            link_name TEXT,
            link TEXT 
            )                            
            ''')

            self.connect.commit()
            print(">Таблица Links успешно создана")
        
        except sqlite3.OperationalError:
            print("\n> Ошибка создания таблицы")
            print(f"->Имя таблицы |Ссылки|")
            print(f"->Название таблицы Links")
    
    # Создание анкеты пользователя
    def create_user(self, vk_user_id:str) -> None:
        connect = sqlite3.connect(self.db_name+".db")
        cursor = connect.cursor()           
        
        user_id_check = cursor.execute('SELECT * FROM UsersForm WHERE user_id LIKE (?)', (vk_user_id,)) 
        
        if len(user_id_check.fetchall()) > 0:
            #print(len(user_id_check.fetchall()))
            return 0
        
        cursor.execute('INSERT INTO UsersForm (user_id) VALUES (?)', (vk_user_id,))
        connect.commit()
        connect.close()                
    
    # Задаем имя пользователю
    def update_user_name(self, vk_user_id:str, user_name:str)->None:
        
        connect = sqlite3.connect(self.db_name+".db")
        cursor = connect.cursor()
        
        cursor.execute('UPDATE UsersForm SET name = ? WHERE user_id = ?', (user_name, vk_user_id))
        
        connect.commit()
        connect.close()
                                           
    # задаем возраст пользователю
    def update_user_age(self, vk_user_id:str, user_age:int)->None:
    
        connect = sqlite3.connect(self.db_name+".db")
        cursor = connect.cursor()

        cursor.execute('UPDATE UsersForm SET age = ? WHERE user_id = ?', (user_age, vk_user_id))

        connect.commit()
        connect.close()
    
    # Задаем город пользователя
    def update_user_city(self, vk_user_id:str, user_city:str)->None:
    
        connect = sqlite3.connect(self.db_name+".db")
        cursor = connect.cursor()

        cursor.execute('UPDATE UsersForm SET city = ? WHERE user_id = ?', (user_city, vk_user_id))

        connect.commit()
        connect.close()   
    
    # Получение данных пользователя
    def get_user_anketa_info(self,vk_user_id:str):
         
        connect = sqlite3.connect(self.db_name+".db")
        cursor = connect.cursor()  
        user_id_check = cursor.execute('SELECT * FROM UsersForm WHERE user_id LIKE (?)', (vk_user_id,)).fetchall()[0]
        
        message = f"Имя: {str(user_id_check[2]).title()}\nГород: {str(user_id_check[3]).title()}\nВозраст: {str(user_id_check[4]).title()}лет"
        
        return message
        
    # Редактирование анкеты
    
    # Сборка бд
    def build_empty_database(self,) -> None:
        
        self.create_database(name_database=self.db_name)
        
        # Создаём таблицу пользователя бота
        self.create_users_form_table()
        
        # Вкладка проекты
        self.create_projects_form_table()
        self.create_project_finder_from_table()
        self.create_callback_projects_form_table()
        self.create_callback_project_finder_from_table()
        
        # Вкладка менторы
        self.create_mentors_profile_from_table()
        self.create_mentors_finder_profile_from_table()
        self.create_callback_mentor_from_table()
        self.create_callback_mentor_finder_from_table()
        
        # Вкладка друзья 
        self.create_just_friends_from_table()
        self.create_callback_frends_from_table()
        
        # Вкладка партнерские предложения
        self.create_partner_offers_from_table()
        self.create_callback_partner_offers_from_table()
        
        
        self.create_links_from_table()
        
        self.create_one_formers_from_table()
        
        
        
        # Таблицы обратной связи
        
        
        
    # Создание бекапов
    def create_backup(self, ) -> None:
        pass
    
    # Подключение резервной БД
    def connect_backup_db(self, path:str=None):
        pass