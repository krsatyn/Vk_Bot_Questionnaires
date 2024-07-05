import sqlite3


class DataBase():
    
    def __init__(self, db_name:str="db") -> None:
        self.db_name = db_name
        
        
    # Создание БД
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
    def create_users_form_table(self, ) -> None:
        '''Создание таблицы
        |id:int key|user_id:str|name:str|city:str|age:int|
        '''
        
        cursor = self.connect.cursor()
        
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS UsersForm (
            id INTEGER PRIMARY KEY,
            user_id TEXT NOT NULL,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            age INTEGER NOT NULL
            )                            
            ''')

            self.connect.commit()
            print(">Таблица UsersForm успешно создана")
        
        except sqlite3.OperationalError:
            print("\n> Ошибка создания таблицы")
            print(f"->Имя таблицы |таблица для анкеты пользователя|")
            print(f"->Навзание таблицы UsersForm")

    # Создание таблицы для анкет проектов
    def create_projects_form_table(self, ) -> None:
        '''Создание таблицы
        |id:int key|user_id:str|project_info:str|find_teams:str|
        '''
        
        cursor = self.connect.cursor()
        
        try:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ProjectsForm (
            id INTEGER PRIMARY KEY,
            user_id TEXT NOT NULL,
            project_info TEXT NOT NULL,
            find_teams TEXT NOT NULL
            )                            
            ''')

            self.connect.commit()
            print(">Таблица ProjectsForm успешно создана")
        
        except sqlite3.OperationalError:
            print("\n> Ошибка создания таблицы")
            print(f"->Имя таблицы |таблица для анкет проектов|")
            print(f"->Навзание таблицы ProjectsForm")

    # Создание таблицы для анкет проектов
    def create_project_form_table(self, ) -> None:
        pass

    # Создание таблицы для анкет проектов
    def create_project_form_table(self, ) -> None:
        pass

    # Создание таблицы для анкет проектов
    def create_project_form_table(self, ) -> None:
        pass

    # Создание таблицы для анкет проектов
    def create_project_form_table(self, ) -> None:
        pass

    # Создание таблицы для анкет проектов
    def create_project_form_table(self, ) -> None:
        pass

    # Создание таблицы для анкет проектов
    def create_project_form_table(self, ) -> None:
        pass

    # Сборка бд
    def build_empty_database(self,) -> None:
        
        self.create_database(name_database=self.db_name)
        self.create_users_form_table()
        self.create_projects_form_table()

    def create_backup(self, ) -> None:
        pass

DB = DataBase()
DB.build_empty_database()