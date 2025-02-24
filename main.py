from func.Chat import Chat
from LLM.ChatGpt import ChatGpt 
# from func.DataOnline import search_google
from func.enhanced_search import genEffect
from func.enhanced_search import  search_google
from func.ListenJs import Listen
from func.SpeakOffline import Speak
import os
if(__name__ == '__main__'):
    while(True):
        query = Listen()
        QL = query.lower()
        # initialize chat
        chat_response = Chat(QL)
        # get data
        data = search_google(QL)
        if data != None:
            Speak(data)
            genEffect(f'\033[1m\033[33mThe result we got:\n{data}\033[0m')
            os.system("pause")
        else:
            Speak(chat_response[0])
            genEffect(f'\033[1m\033{chat_response[0]}\033[0m')