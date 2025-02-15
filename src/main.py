import pyttsx3 as tts
import speech_recognition as sr

# windows sapi5 voice engine
def initialize_engine():
    engine = tts.init('sapi5')
    # to voices are available - 0(male) and 1(female) engine ids
    voices = engine.getProperty('voices') 
    engine.setProperty('voice',voices[1].id)
    # rate of the voices
    rate = engine.getProperty('rate')
    engine.setProperty('rate',rate-50)
    # volume of voices
    volume = engine.getProperty('volume')
    engine.setProperty('volume',volume+0.25) # increasing 25% of volume
    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()
def command():
    # recoginze the voice
    r = sr.Recognizer()
    # take input from microphone as source
    with sr.Microphone() as source:
        # adjusting the ambient noise coming fro our microphone
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening ...")
        # if we are not speaking up on to our mic then pause
        ''' Properties for recognizers '''
        r.pause_threshold = 1.0
        r.phrase_threshold = 0.3
        r.sample_rate = 4800
        r.dynamic_energy_threshold = True
        r.operation_timeout = 5
        r.non_speaking_duration = 0.5
        r.dynamic_energy_adjustment_damping = 2
        r.energy_threshold = 150
        r.phrase_time_limit = 10
        # print all the microphones list
        # print(sr.Microphone.list_microphone_names())
        # take input audio 
        audio = r.listen(source,timeout=5, phrase_time_limit=10)
        try:
            print("Recognizing ...")
            # requires internet-connection
            query = r.recognize_google(audio, language = 'en-in')
            print(f"Looking for [\'{query}\']")
        except Exception as e:
            print('Can u come up again please ...')
            return "None"
        return query

if __name__ == '__main__':
    while True:
        query = command().lower()
        print(query)
# speak("Hello I'm rete.x")

