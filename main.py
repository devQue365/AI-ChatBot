from func.Chat import Chat
from LLM.SAMgpt import SAM, Filter
# from func.DataOnline import search_google
from func.enhanced_search import genEffect
from func.enhanced_search import  search_google
from func.ListenJs import Listen
from func.SpeakOffline import Speak
from func.ocr import ocr_v1_clk # Variant-1
import os
import re
os.system("pip install -U g4f") # install this ...
if(__name__ == '__main__'):
    while(True):
        query = Listen()
        # query = input("Enter query : ")
        QL = query.lower()
        len_Q = len(query.split(" "))
        start_Q = QL.split(" ")[0]
        end_Q = query.split(" ")[-1]

        # Check for OCR request
        if(start_Q == "click" or (start_Q == "double" and "click" in query)) and len_Q<7:
            # remove unwanted chunks
            QL = QL.replace("click","").replace("on","").replace("sam", "").replace("double", "")
            if(start_Q == "double"):
                response = ocr_v1_clk(QL.strip(),double_click=True)
            else:
                response = ocr_v1_clk(QL.strip())

            genEffect('\033[1m\033[33m'+response+'\033[0m')
            Speak(response)
        elif("bob" in start_Q):
            _code = SAM(query, "*** Use python programming language. Just write complete code nothing else")
            _code = Filter(_code)
            exec(_code)
        elif("search internet" in QL):
            QL =  re.sub(r'^.*?\bfor\b\s*', '', QL, flags=re.IGNORECASE)
            response = search_google(QL.strip())
            genEffect('\033[1m\033[33m'+response+'\033[0m')
            Speak(response)
        else:    
            response = SAM(query+"*** Reply in brief short way like SAM without telling the user ***")
            if response:
                genEffect('\033[1m\033[33m'+response+'\033[0m')
                Speak(response)
            elif Chat(QL)[1]>0.99:
                response  = Chat(QL)[0]
                genEffect('\033[1m\033[33m'+response+'\033[0m')
                Speak(response)
        os.system("pause")
    