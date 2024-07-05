import vk_api as vk


from vk_api.longpoll import VkLongPoll, VkEventType
from setting import token 

if __name__ == "__main__":
    
    vk_session = vk.VkApi(token=token)
    session_api = vk_session.get_api()
    longpool = VkLongPoll(vk_session)
    

def send_some_msg(id, some_text):
    vk_session.method("messages.send", {"user_id":id, "message":some_text, "random_id":0})
    

for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            msg = event.text.lower()
            id = event.user_id
            if msg == "kurwa":
                send_some_msg(id, "kurwa")