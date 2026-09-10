# tts_worker.py
import sys
import time
import pyttsx3

try:
    def speak_argument():
        if len(sys.argv) < 2: # this if statment checks if the script was actully parsed the text the read out
            print("Error: No text provided to speak.")
            return

        # this combines all the arguments into a signl string
        text_to_speak = " ".join(sys.argv[1:])

        # runs the pyttsx3 text to speech engine
        engine = pyttsx3.init()
        engine.say(text_to_speak)
        engine.runAndWait()
        engine.stop()

        time.sleep(1)
        sys.exit()

    if __name__ == "__main__":
        speak_argument()

except Exception as e:
    print(f"Exception: {e}")

except KeyboardInterrupt:
    print("Programed killed")
    sys.exit()
