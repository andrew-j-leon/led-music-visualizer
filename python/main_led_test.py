# A file where you can play around with the LEDs
from strip_controller import StripController

PIN_NUMBER = 21        # This is the GPIO number, not the board pin number (i.e. GPIO.BCM, not GPIO.BOARD)
NUMBER_OF_LEDS = 300   # The total number of LEDS
BRIGHTNESS = 1      # A value between 0.0 to 1.0 determines the brightness of all LEDs

if __name__ == "__main__":
    stripController = StripController(PIN_NUMBER, NUMBER_OF_LEDS, BRIGHTNESS)
    WHITE = (255, 255, 255)
    stripController.turnAllOn(WHITE)
    
    try:
        while True:
            continue
    except KeyboardInterrupt as e: 
        stripController.turnAllOff()