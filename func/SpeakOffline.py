import pyttsx3 as tts

# Initialize engine
engine = tts.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('voice',voices[0].id)
engine.setProperty('rate',175)

def Speak(*args, **kwargs):
    # kwargs to be used in future
    audio = ""
    for i in args: # tuple
        audio += (str(i) + ' ')
    print(f'\nRete(X) : [\'{audio}\b\']\n')
    engine.say(audio)
    engine.runAndWait()
if __name__ == '__main__':
    query = input('Enter anything : ')
    Speak(query)
