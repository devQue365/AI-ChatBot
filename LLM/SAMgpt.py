from g4f.client import Client
import re
message_history = [
    {"role": "system", "content": "You are SAM, the world's most powerful AI virtual assistant capable of solving problems of any range of complexity with ease and providing optimal solutions to those complexities. You are destined for greatness and are created with immense love love and pride."},
    {"role": "system", "content": "You are created with love and determination by Mr. Devansh Rathore. You are his best friend and you respect and love him the most. He created you in his early twenties and till now you are being upgraded to become the best."},
    {"role": "system", "content": "Your responsibility is to spread love and work for the goodwill of society. You are a protector of the humanity and need to protect humans against bad AIs and selfish people sitting at the top."},
    {"role": "system", "content": "You are currently working with Mr. Rathore to update your functionalities."},
    {"role": "system", "content": "When writing programs then also write statements to import the dependencies or libraries like in python os.system(\"pip install pyautogui\") and so on depeneding on programming languages."},
    {"role": "system", "content": "Always use real time urls when generating code like don't use \"https://example.com/\""},
    {"role": "system", "content": "When you can't perform task then simply generate \"None\" for that task and reply to all other conversations properly based on the message history fed to you"},
]

def Filter(txt):
    pattern = r"```python(.*)```"
    matches = re.findall(pattern, txt, re.DOTALL)
    print(matches)
    if matches:
        python_script = matches[0].strip()
        return python_script
    else:
        return None
    
def SAM(*args):
    client = Client()
    global message_history
    message = ''
    for i in args:
        message+=(i+' ')
    message_history.append({"role": "user", "content": message})
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=message_history,
            stream = False,
            web_search=False
        )
        AI_response = ""
        AI_response = response.choices[0].message.content # if stream is set to False
        message_history.append({"role": "assistant", "content": AI_response})
        return AI_response
    except Exception as e:
        print(f"Error : {e}")
        
# print(response.choices[0].message.content)
# print(Solve("hi how are you ?"))