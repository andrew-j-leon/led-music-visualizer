import neopixel
import board


class StripController:
    """
    A controller for the RGB strip. Allows the user to turn on/off
    LEDs and change their color.
    """
    def  __init__(self, pinNumber, numberOfLEDs, brightness):
        """
        Create a controller for the RGB strip.
        
        @param {int}   pinNumber     : The GPIO number, not the board pin number (i.e. GPIO.BCM, not GPIO.BOARD).
                                       Valid GPIO pins are  10, 12, 18, & 21 (according to https://learn.adafruit.com/neopixels-on-raspberry-pi?view=all ,
                                       18 is the standard pin).
        @param {int}   numberOfLEDs  : The total number of LEDs on the RGB strip.
        @param {float} brightness    : Value between 0.0 to 1.0 that determines the brightness of all LEDs. Lower = dimmer.
        """
        # pin        : The GPIO number (GPIO.BCM, not GPIO.Board).
        # n          : Total number of LEDs on the RGB strip.
        # auto_write : You must call pixels.show() before your changes show up.
        # brightness : Value between 0.0 to 1.0 that determines the brightness of all LEDs.        
        GPIO_pin = self._getGPIO_pinNumber(pinNumber)
        self.pixels = neopixel.NeoPixel(pin=GPIO_pin, n=numberOfLEDs, auto_write=False, brightness=brightness)
        
    def setBrightness(self, brightness):
        self.pixels.brightness = brightness
    
    def _getGPIO_pinNumber(self, pinNumber):
        """
        Convert a GPIO pin number (int) to a board.D(pin number) object.
        Accepts only 10, 12, 18, and 21.
        
        @param {int} pinNumber : A GPIO pin number.
        @return {board.GPIO}   : An object that specifies a GPIO number.
        
        @throws {ValueError}   : Thrown if an invalid number is given.
        """
        if (not pinNumber in (10, 12, 18, 21)):
            raise ValueError("Pin number must be 10, 12, 18, or 21")
        
        if (pinNumber == 10):
            return board.D10
        elif (pinNumber == 12):
            return board.D12
        elif (pinNumber == 18):
            return board.D18
        else:
            return board.D21
        
    def length(self):
        """
        @return {int} : The total number of LEDs on the RGB strip.
        """
        return len(self.pixels)
        
    def turnOn(self, startLED, endLED, RGB):
        """
        Turn on LEDs from/to [startLED, endLED] with the given RGB color.
        If an LED is already on, changes its color to the given RGB color.
            - If startLED < 0, startLED is treated as 0.
            - If endLED > numberOfLEDs - 1, endLED is treated as numberOfLEDs - 1.
        
        Ex: turnOn(0, 4, (255, 0, 0)) sets LEDs 0, 1, 2, 3, & 4 to R=255, G=0, & B=0
            (i.e. red).
        
        @param {int} startLED             : The index of the lower-bound LED (indexing begins at 0).
        @param {int} endLED               : The index of the upper-bound LED (indexing begins at 0).
        @param {tuple<int, int, int>} RGB : Describes the RGB color (RGB[0] = red; RGB[1] = green; RGB[2] = blue).        
        """
        startIndex = startLED if startLED >= 0 else 0
        endIndex = endLED if endLED <= self.length() - 1 else self.length() - 1
        
        for i in range(startIndex, endIndex):
            self.pixels[i] = RGB
        self.pixels.show()
    
    def turnOff(self, startLED, endLED):
        """
        Turn off LEDs from/to [startLED, endLED] Similar to using turnOn(...) with
        RGB = (0,0,0).
        
        @param {int} startLED : The index of the lower-bound LED (indexing begins at 0).
        @param {int} endLED   : The index of the upper-bound LED (indexing begins at 0).
        """
        self.turnOn(startLED, endLED, (0,0,0))
        
    def turnAllOn(self, RGB):
        """
        Turn on all LEDs and sets them to the given RGB color.
        If an LED is already on, changes its color to the given RGB color.
        
        @param {tuple<int, int, int>} RGB : Describes the RGB color (RGB[0] = red; RGB[1] = green; RGB[2] = blue).   
        """
        self.pixels.fill(RGB)
        self.pixels.show()    
    
    def turnAllOff(self):
        """
        Turns all LEDs off.
        """
        self.pixels.fill((0,0,0))
        self.pixels.show()
    
        
        
        
