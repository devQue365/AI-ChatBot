import speech_recognition as sr

#Initialize reecognizer
recorgnizer = sr.Recognizer()

def Listen():
    # using default microphone as the source
    with sr.Microphone() as source: # implicit closing
        print("Listening ...")

        # adjust ambient noise
        recorgnizer.adjust_for_ambient_noise(source)
        # listen to user's input
        audio_data = recorgnizer.listen(source)

        try:
            print("Recognizing ...")
            # Recognize speech using Google Speech Recognition
            text = recorgnizer.recognize_google(audio_data)
            print(f"Looking for [\'{text}\']")
            return text
        except sr.UnknownValueError:
            # could not understand the audio
            print("Can you please come up again ...")
            return None
        except sr.RequestError as e:
            # if in case the internet connection breaks
            print(f"Error : {e}")
            return None
if __name__ == '__main__':
    recogninez_text = Listen()
    