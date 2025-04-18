import threading # Backbone of this project
# from func.Chat import Chat
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

def execute_request(QL):
    _code = SAM(QL, "*** Use python programming language. Just write complete code nothing else")
    _code = Filter(_code)
    try:
        exec(_code)
    except Exception as e:
        genEffect(f'\033[1m\033[33mError while handling your request ....\n{e}\033[0m')

if(__name__ == '__main__'):
    while(True):
        query = Listen()
        # query = input("Enter query : ")
        QL = query.lower()
        len_Q = len(query.split(" "))
        start_Q = QL.split(" ")[0]
        # end_Q = query.split(" ")[-1]

        # Send the query first to GPT
        response = SAM(query+"*** Reply in brief short way like SAM without telling the user ***")
        if(response != "SAMi()"):
            genEffect('\033[1m\033[33m'+response+'\033[0m')
            # Speak(response)
        else:
            # check for OCR
            if(("click" in QL) or ("double" and "click" in QL)):
                def extract_clickable_elements(text):
                    # used regex to match clickable elements
                    pattern = r'(?i)(?:click on\s+)([A-Za-z0-9\s]+?)(?=\s*(?:and|,|\.|$))'
                    # Extract clickable elements
                    elements = re.findall(pattern, text)
                    return [element.strip() for element in elements]
                clickables = extract_clickable_elements(QL)
                # print(clickables)
                os.system("clear")
                for clickable in clickables:
                    response = ocr_v1_clk(clickable)
                    genEffect('\033[1m\033[33m'+response+'\033[0m')
                    Speak(response) 
                
            # elif(re.search(r'(?i)^.*?\b(open|play|search|quick|create)',QL, re.IGNORECASE)):
            else:
                # check for quick search
                if("quick" in QL and "search" in QL):
                    QL =  re.sub(r'^.*?\bfor\b\s*', '', QL, flags=re.IGNORECASE)
                    response = search_google(QL.strip())
                    genEffect('\033[1m\033[33m'+response+'\033[0m')
                    Speak(response)
                else:
                    # create a thread for this task
                    threading.Thread(target = execute_request, args = (QL,), daemon=True).start()
                    genEffect("I am performing tasks in the background, you can continue to add next input friend ...")
            # elif Chat(QL)[1]>0.99:
            #     genEffect("\033[1m\033[35mSwitched to SAM (__BASE__)\033[0m")
            #     response  = Chat(QL)[0]
            #     genEffect('\033[1m\033[33m'+response+'\033[0m')
                Speak(response)

    