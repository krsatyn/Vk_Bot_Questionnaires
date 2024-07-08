import vk_api as vk
import text_message
import sqlite3

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from setting import token 
from database_func import DataBase

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

for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            msg = event.text.lower()
            id = event.user_id
            
            if msg == "начать":
                keyboard = VkKeyboard(one_time=True, )
                keyboard.add_button(label="Приступим",color=VkKeyboardColor.POSITIVE)
                send_some_message(id, text_message.start_message['hello_message'], keyboard)
                
            if msg == "приступим":
                try:
                    keyboard = VkKeyboard(one_time=True, )
                    
                    send_some_message(id=id, some_text=text_message.user_form_message["name_question"])
                    
                    db.create_user(str(event.user_id))
                    key_word = ">name"
                 
                except (sqlite3.ProgrammingError, sqlite3.OperationalError) as error_message:
                    send_some_message(id, some_text="Ошибка:\n" + (error_message))
                    
            if key_word == ">name":
                db.post_user_name(msg)
                key_word=">age"
                pass
            
            if key_word == ">age":
                print(2)
            
            if key_word== "city":
                pass
            