import speech_recognition as sr

#Initialize reecognizer
recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.5
def Listen():
    # using default microphone as the source
    with sr.Microphone() as source: # implicit closing
        print("Listening ...")

        # adjust ambient noise
        recognizer.adjust_for_ambient_noise(source)
        # listen to user's input
        audio_data = recognizer.listen(source)

        try:
            print("Recognizing ...")
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio_data)
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
    