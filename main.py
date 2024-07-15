# main.py

import copy
import vk_api as vk
import text_message
import sqlite3

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from setting import token 
from database_func import DataBase
from src.anketa.ankenta import AnketaConstruct

db = DataBase() # подключаем бд

if __name__ == "__main__":
    
    vk_session = vk.VkApi(token=token)
    session_api = vk_session.get_api()
    longpool = VkLongPoll(vk_session)

def send_some_message(id, some_text, keyboard=None):
    
    post = {
        "user_id":id, 
        "message":some_text, 
        "random_id":0,}

    if keyboard != None:
        post['keyboard'] = keyboard.get_keyboard() 
        
    vk_session.method("messages.send", post)
    
key_word = ""

setting_dict = {"db":db,
                "table_name":"",
                "instruction":{"start":"",},
                "create_kw":"",
                "message_instruction":{"start":""}}

'''
# Анкета 1
setting_dict_1 = copy.deepcopy(setting_dict) # копирование элемента словаря
setting_dict_1['table_name'] = 'JustFriends'
setting_dict_1['instruction']['start'] = 'just_friends_info'
setting_dict_1['create_kw'] = 'приступаем к тестированию!'
setting_dict_1['message_instruction']['start'] = "Опиши своего друга"


# Анкета 2
setting_dict_2 = dict(setting_dict) # копирование элемента словаря

setting_dict_2['create_kw'] = 'приступаем к тестированию!'

setting_dict_2['table_name'] = 'ProjectsForm'

setting_dict_2['instruction']['start'] = 'project_name'
setting_dict_2['instruction']['info'] = 'project_info'
setting_dict_2['instruction']['teams'] = 'find_teams'

setting_dict_2['message_instruction']['start'] = "Напишите название проекта"
setting_dict_2['message_instruction']['info'] = "Опишите ваш проект"
setting_dict_2['message_instruction']['teams'] = "Опишите кого вы ищете"
'''
section_kw = ""

for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        
            msg = event.text.lower()
            id = event.user_id
            
            # Стартовое сообщение
            if msg == "начать":
                keyboard = VkKeyboard(one_time=True, )
                keyboard.add_button(label="Приступим",color=VkKeyboardColor.POSITIVE)
                send_some_message(id, text_message.start_message['hello_message'], keyboard)
            
            # Начало заполнение основной анкеты    
            if msg == "приступим":
                try:
                    keyboard = VkKeyboard(one_time=True, )
                    
                    send_some_message(id=id, some_text=text_message.user_form_message["name_question"])
                    
                    db.create_user(str(event.user_id))
                    
                    # Первое меню
                    key_word = ">name"
                    #send_some_message(id=id, some_text=text_message.user_form_message["name_question"])

                except (sqlite3.ProgrammingError, sqlite3.OperationalError) as error_message:
                    send_some_message(id, some_text="Ошибка:\n" + (error_message))
            
            # Заполнение возраста пользователя
            if (key_word == ">age") and (text_message.msg_list.count(msg) == 0):
               
                try:
                    msg = int(msg)
                    db.update_user_age(vk_user_id=id, user_age=msg)
                    key_word=""
                    send_some_message(id=id, some_text=f'Анкета заполнена')
                    
                    keyboard_menu = VkKeyboard(one_time=True, )
                    
                    keyboard_menu = VkKeyboard(one_time=True)
                    keyboard_menu.add_button(label="Собрать или присоединиться к проектам", color=VkKeyboardColor.POSITIVE)
                    keyboard_menu.add_line()
                    keyboard_menu.add_button(label="Найти или стать наставником")
                    keyboard_menu.add_line()
                    keyboard_menu.add_button(label="Партнерские предложения (для проектов)")
                    keyboard_menu.add_line()
                    keyboard_menu.add_button(label="Найти друзей")
                    keyboard_menu.add_line()
                    keyboard_menu.add_button(label="Моя анкета")

                    send_some_message(id, "Ты в меню", keyboard_menu)
                    
                    
                except ValueError:
                   send_some_message(id=id, some_text=f'Введи возраст цифрой')
            
            # Заполнение города пользователя
            if (key_word== ">city") and (text_message.msg_list.count(msg) == 0):
                db.update_user_city(vk_user_id=id, user_city=msg)
                key_word=">age"
                send_some_message(id=id, some_text=f'Сколько тебе лет?')
            
            # Заполнение имени пользователя       
            if (key_word == ">name") and (text_message.msg_list.count(msg) == 0):
                
                db.update_user_name(vk_user_id=id, user_name=msg)
                send_some_message(id=id, some_text=f'Хорошо, {msg.capitalize()}. Откуда ты?')
                key_word=">city"
            
            # основное меню
            if (msg == '/menu') or (msg == "назад в меню"):
                keyboard_menu = VkKeyboard(one_time=True)
                keyboard_menu.add_button(label="Собрать или присоединиться к проектам", color=VkKeyboardColor.POSITIVE)
                keyboard_menu.add_line()
                keyboard_menu.add_button(label="Найти или стать наставником")
                keyboard_menu.add_line()
                keyboard_menu.add_button(label="Найти друзей или однофорумчан") # обьединить с функцией найти друзей
                keyboard_menu.add_line()
                keyboard_menu.add_button(label="Партнерские предложения для проектов") # проверить
                keyboard_menu.add_line()
                keyboard_menu.add_button(label="Моя анкета")
                
                send_some_message(id, "Ты в меню", keyboard_menu)
                
                section_kw = ''
            
                
            if msg == 'собрать или присоединиться к проектам':
                keyboard_project_menu = VkKeyboard(one_time=True)
                keyboard_project_menu.add_button(label="Собрать команду в проект", color=VkKeyboardColor.POSITIVE)
                keyboard_project_menu.add_line()
                keyboard_project_menu.add_button(label="Присоединиться к проекту")
                keyboard_project_menu.add_line()
                keyboard_project_menu.add_button(label="Назад в меню", color=VkKeyboardColor.NEGATIVE)
                send_some_message(id, "Ты в меню Проектов", keyboard_project_menu)
            
            if (msg == "собрать команду в проект"):

                    section_kw = "project_anketa"
                    anketa_setting_dict = copy.deepcopy(setting_dict)
                    anketa_setting_dict['create_kw'] = 'cобрать команду в проект'

                    anketa_setting_dict['table_name'] = 'ProjectsForm'

                    anketa_setting_dict['instruction']['start'] = 'project_name'
                    anketa_setting_dict['instruction']['info'] = 'project_info'
                    anketa_setting_dict['instruction']['teams'] = 'find_teams'

                    anketa_setting_dict['message_instruction']['start'] = "Напишите название проекта"
                    anketa_setting_dict['message_instruction']['info'] = "Опишите ваш проект"
                    anketa_setting_dict['message_instruction']['teams'] = "Опишите кого вы ищете"
                
                    project_anketa = AnketaConstruct(session_api=session_api,
                                                     vk_session=vk_session,
                                                     longpool=longpool,
                                                     setting_dict=anketa_setting_dict) 
            if section_kw == "project_anketa":
                project_anketa.main(vk_user_id=id, msg=msg)
                    
            if msg == 'найти или стать наставником':
                keyboard_mentor_menu = VkKeyboard(one_time=True)
                keyboard_mentor_menu.add_button(label="Найти наставника", color=VkKeyboardColor.POSITIVE)
                keyboard_mentor_menu.add_line()
                keyboard_mentor_menu.add_button(label="Стать наставником")
                keyboard_mentor_menu.add_line()
                keyboard_mentor_menu.add_button(label="Назад в меню", color=VkKeyboardColor.NEGATIVE)
                send_some_message(id, "Ты в меню проектов", keyboard_mentor_menu)
            
            if msg == 'найти друзей или однофорумчан':
                keyboard_frends_and_forum_member_menu = VkKeyboard(one_time=True)
                keyboard_frends_and_forum_member_menu.add_button(label="Найти друзей")
                keyboard_frends_and_forum_member_menu.add_line()
                keyboard_frends_and_forum_member_menu.add_button(label="Найти однофорумчан")
                keyboard_frends_and_forum_member_menu.add_line()
                keyboard_frends_and_forum_member_menu.add_button(label="Назад в меню", color=VkKeyboardColor.NEGATIVE)
                send_some_message(id, "Ты в меню поиска друзей или однофорумчан\n(не думай что ты найдешь их тут, у тебя их не может быть даже в теории. KEKWA)", keyboard_frends_and_forum_member_menu)
            
            if msg == 'партнерские предложения для проектов':
                keyboard_partner_offer_menu = VkKeyboard(one_time=True)
                keyboard_partner_offer_menu.add_button(label="Предложить партнерку")
                keyboard_partner_offer_menu.add_line()
                keyboard_partner_offer_menu.add_button(label="Назад в меню", color=VkKeyboardColor.NEGATIVE)
                send_some_message(id, "Ты в меню настроек партнерские предложений для проектов", keyboard_partner_offer_menu)
  
            if msg == 'моя анкета' and section_kw=="":
                keyboard_my_anketa_menu = VkKeyboard(one_time=True)
                keyboard_my_anketa_menu.add_button(label="Редактировать мою анкету", color=VkKeyboardColor.POSITIVE)
                keyboard_my_anketa_menu.add_line()
                keyboard_my_anketa_menu.add_button(label="Назад в меню", color=VkKeyboardColor.NEGATIVE)
                message = db.get_user_anketa_info(vk_user_id=id)
                send_some_message(id, message, keyboard_my_anketa_menu)
                
            if (msg == 'редактировать мою анкету'):
                keyboard_redact_my_anketa = VkKeyboard(one_time=True)
                keyboard_redact_my_anketa.add_button(label="Имя")
                keyboard_redact_my_anketa.add_line()
                keyboard_redact_my_anketa.add_button(label="Возраст")
                keyboard_redact_my_anketa.add_line()
                keyboard_redact_my_anketa.add_button(label="Город")
                keyboard_redact_my_anketa.add_line()
                keyboard_redact_my_anketa.add_button(label="Заполнить анкету заново")
                keyboard_redact_my_anketa.add_line()
                keyboard_redact_my_anketa.add_button(label="Назад в меню", color=VkKeyboardColor.NEGATIVE)
                send_some_message(id, "Выбирай что меняем:", keyboard_redact_my_anketa)
            
            #if (msg =="qwe") or (msg == "приступаем к тестированию!") or (text_message.msg_list.count(msg) == 0):
            #    
            #    keyboard_test = VkKeyboard(one_time=True)
            #    keyboard_test.add_button(label="приступаем к тестированию!", color=VkKeyboardColor.NEGATIVE)
            #    send_some_message(id, "МЫ В ТЕСТОВОЙ ЗОНЕ, ЩА ВСЕ ПОЙДЕТ !!!", keyboard_test) 
            #    
            #    
            #    
            #    #anketa.main(msg=msg, vk_user_id=id)
                