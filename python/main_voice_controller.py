'''
Created on Jul 15, 2020

@author: Andrew Leon
'''

import speech_recognition as sr
import pyttsx3
from strip_controller import StripController

AMBIENT_NOISE_ADJUSTMENT_TIME = 2 # In seconds

PIN_NUMBER = 21        # This is the GPIO number, not the board pin number (i.e. GPIO.BCM, not GPIO.BOARD)
NUMBER_OF_LEDS = 300   # The total number of LEDS
BRIGHTNESS = 0.05      # A value between 0.0 to 1.0 determines the brightness of all LEDs


def textToSpeech(text):
    """
    @param {string} text
    """
#     engine = pyttsx3.init()
#     engine.say(text)
#     engine.runAndWait()
    print("Raspberry Pi says: {}".format(text))
    
def handleCommand(command, stripController):
    """
    @param {string} command
    
    @return {bool} : True if shut down; False if otherwise.
    """
    if ("on" in command.lower()):
        textToSpeech("Turning on the lights.")
        stripController.turnAllOn((254, 254, 254))
        
    elif ("off" in command.lower()):
        textToSpeech("Turning off the lights.")
        stripController.turnAllOff()
    
    elif (command.lower() in ("shut down", "shutdown", "power down", "power off")):
        textToSpeech("Shutting down...")
        stripController.turnAllOff()
        return True
        
    else:
        textToSpeech("Sorry. I didn't understand that.")
        
    return False

recognizer = sr.Recognizer()
stripController = StripController(PIN_NUMBER, NUMBER_OF_LEDS, BRIGHTNESS)
finished = False

with sr.Microphone() as microphone:
    while not finished:
        try:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(microphone, AMBIENT_NOISE_ADJUSTMENT_TIME)            
            print("Listening for 'raspberry pi'...")
            audio = recognizer.listen(microphone)
            print("Sending command to Google API...")
            text = recognizer.recognize_google(audio)
            print("Did you say: {}".format(text))
            
            if ("raspberry pi" in text.lower()):
                while True:
                    try:
                        print("Listening for command...")
                        audio = recognizer.listen(microphone)
                        print("Sending command to Google API...")
                        text = recognizer.recognize_google(audio)
                        print("Did you say: {}".format(text))
                        finished = handleCommand(text, stripController)
#                         finished = handleCommand(text, False)
                        
                        break 
                        
                    except sr.RequestError as e:
                        textToSpeech("Couldn't request results")
                        print(e)
                        
                    except sr.UnknownValueError as e:
                        textToSpeech("Unknown error occurred")
                        print(e)             
                
            
        except sr.RequestError as e:
            textToSpeech("Couldn't request results")
            print(e)
            
        except sr.UnknownValueError as e:
            textToSpeech("Unknown error occurred")
            print(e)
        
        
        
        
        