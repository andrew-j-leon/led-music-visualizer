from amplitude_visualizer import AmplitudeVisualizer
from strip_controller import StripController
from color_shifter import ColorShifter

class CenterDoubleBarVisualizer(AmplitudeVisualizer):
    """
    A music visualizer where lights are in the center of the LED strip
    and 2 bars radiate from this center. The LEDs colors will also shift
    through the spectrum.
    """
    
    def __init__(self, pinNumber, numberOfLEDs, brightness):
        """
        Create a visualizer that uses average amplitude data.
        
        @param {int}   pinNumber      : The GPIO number, not the board pin number (i.e. GPIO.BCM, not GPIO.BOARD).
                                        Valid GPIO pins are  10, 12, 18, & 21 (according to https://learn.adafruit.com/neopixels-on-raspberry-pi?view=all ,
                                        18 is the standard pin).
        @param {int}   numberOfLEDs   : The total number of LEDs on the RGB strip.
        @param {float} brightness     : Value between 0.0 to 1.0 that determines the brightness of all LEDs. Lower = dimmer.
        """
        AMP_THRESHOLD = 45     # The amplitude value at which to start lighting up LEDs. Useful when the played .wav file
                               # is normally at a certain amplitude.
        LED_PER_AMP = 3.8      # This value scales the number of LEDs that are lit for each amplitude value above START_AMPLITUDE.
                               # Ex: If set to 1, 1 LED is lit for each amp value. If set to 4, 4 LEDs are lit for each amp value.
        SATURATION = 85
        LIGHTNESS = 45
        
        self.previousAvgAmp = 0.0
        self.currentAvgAmp = 0.0
        self.ampThreshold = AMP_THRESHOLD
        self.ledPerAmp = LED_PER_AMP
        self.stripController = StripController(pinNumber, numberOfLEDs, brightness)
        self.colorShifter = ColorShifter(SATURATION, LIGHTNESS)
        
        self.colorUpdateCounter = 0
        
    def setHueRange(self, hueRange):
        """
        Set the hue range that the LEDs cycle through.
        
        @param hueRange {list<int, int>} : The hue range. Properties include...
                                           - hueRange[0] == min hue value
                                           - hueRange[1] == max hue value
                                           - hueRange[0] <= hueRange[1]
                                           - hue values range : [0, 360]
        """
        self.colorShifter.setHueRange(hueRange)
        
    def setShiftType(self, shiftType):
        """
        Set the manner in which the LED lights shift between HSL color hues.
        
        @param {string} shiftType: Strings include...
                                   - "loop"   : Loop through hues.
                                   - "bounce" : Back and forth through hues.
        """
        self.colorShifter.setShiftType(shiftType)
        
    def setAmpThreshold(self, ampThreshold):
        """
        Sets the amp threshold (the amplitude at which LEDs start turning on).
        
        @param {int} ampThreshold : The amp threshold.
        """
        self.ampThreshold = ampThreshold
    
    def setLEDPerAmp(self, ledPerAmp):
        """
        Sets the number of LEDs that get lit per amplitude on both sides of the center
        (e.g. if set to 1, 2 LEDs on both sides of the center will turn on per amp).
        
        @param {int} ledPerAmp : The number of LEDs that get lit per amplitude on both sides
                                 of the center.
        """
        self.ledPerAmp = ledPerAmp
    
    def setBrightness(self, brightness):
        """
        Sets the brightness of the LEDs.
        
        @param {float} brightness : Value between 0.0 to 1.0 that determines the brightness of 
                                    all LEDs. Lower = dimmer.
        """
        self.stripController.setBrightness(brightness)
    
    def setSaturation(self, saturation):
        """
        Sets the HSL saturation of the LED colors.
        
        @param {int} saturation : The HSL Saturation value [0, 100].
        """
        self.colorShifter.setSaturation(saturation)
    
    def setLightness(self, lightness):
        """
        Sets the HSL lightness of the LED colors.
        
        @param {int} lightness : The HSL Lightness value [0, 100].
        """
        self.colorShifter.setLightness(lightness)
    
    def _getColor(self):
        """
        @return {tuple<int, int, int>} RGB : The next LED color as an RGB color 
                                             (RGB[0] = red; RGB[1] = green; RGB[2] = blue).   
        """
        result = self.colorShifter.getRGB()
        return tuple(result)
    
    def turnOff(self):
        """
        Turns off the LED strip.
        """
        self.stripController.turnAllOff()    
        
    def update(self, nextAvgAmp):
        """
        Updates the LED strip based on the next average amplitude data.
         
        @param {float} nextAvgAmp : The next average amplitude.
        """                
        self.previousAvgAmp = self.currentAvgAmp
        self.currentAvgAmp = nextAvgAmp
          
        centerLED = int(self.stripController.length()/2)
        
        previousAvgAmpInt = int((self.previousAvgAmp - self.ampThreshold) * self.ledPerAmp)
        previousAvgAmpInt = previousAvgAmpInt if (previousAvgAmpInt >= 0) else 0
        
        currentAvgAmpInt = int((self.currentAvgAmp - self.ampThreshold) * self.ledPerAmp)
        currentAvgAmpInt = currentAvgAmpInt if (currentAvgAmpInt >= 0) else 0
         
        # The avg amp increased; we must turn on some LEDs
        if (previousAvgAmpInt < currentAvgAmpInt):
            leftmostBounds = centerLED - currentAvgAmpInt
            rightmostBounds = centerLED + currentAvgAmpInt
            
            self.stripController.turnOn(leftmostBounds, rightmostBounds, self._getColor())
              
        # The avg amp decreased; we must turn off some LEDs
        if (previousAvgAmpInt > currentAvgAmpInt):
            leftmostBounds = centerLED - previousAvgAmpInt
            leftBounds = centerLED - currentAvgAmpInt
              
            rightBounds = centerLED + currentAvgAmpInt
            rightmostBounds = centerLED + previousAvgAmpInt
              
            self.stripController.turnOff(leftmostBounds, leftBounds)
            self.stripController.turnOff(rightBounds, rightmostBounds)

        # Finally, we update the color shifter
        self._updateColorShifter()
        
    def _updateColorShifter(self):
        """
        Updates the color shifter's next color every 3 function calls.
        """
        COUNTER_THRESHOLD = 2
        if (self.colorUpdateCounter >= COUNTER_THRESHOLD):
            self.colorShifter.update()
            self.colorUpdateCounter = 0
        else:
            self.colorUpdateCounter += 1
            
    
        
        
        
        