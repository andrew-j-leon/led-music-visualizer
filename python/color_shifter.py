import colorsys
from math import floor


class ColorShifter:
    """
    A class that handles shifting LED colors.
    """
    class Color:
        def __init__(self, hue, saturation, lightness):
            """
            Construct an object that stores a HSL color.
            
            @param {int} hue        : The HSL hue [0, 360].
            @param {int} saturation : The HSL saturation [0, 100].
            @param {int} lightness  : The HSL lightness [0, 100].
            """
            self.hue = hue
            self.saturation = saturation
            self.lightness = lightness
            
        def setHue(self, hue):
            """
            Set the HSL color hue.
            
            @param {int} hue : HSL color hue [0, 360].
            """
            self.hue = hue
            
        def setSaturation(self, saturation):
            """
            Set the HSL color saturation.
            
            @param {int} saturation : HSL color saturation [0, 100].
            """
            self.saturation = saturation
        
        def setLightness(self, lightness):
            """
            Set the HSL color lightness.
            
            @param {int} lightness : HSL color lightness [0, 100].
            """
            self.lightness = lightness

        def getHue(self):
            """
            @return {int} : This Color's HSL hue.
            """
            return self.hue
            
        def getRGB(self):
            """
            @return {list<int, int, int>} : The representation of this Color using
            RGB values. Indicies include...
                - [0] : red value [0, 255]
                - [1] : green [0, 255]
                - [2] : blue [0, 255]
            """
            # The colorsys library wants decimal values for hue, saturation, and lightness
            hue = self.hue / 361.0                # hue has 361 values [0 degrees, 360 degrees]
            saturation = self.saturation / 101.0  # saturation has 100 values [0%, 100%]
            lightness = self.lightness / 101.0    # lightness has 100 values [0%, 100%]
            
            # Each rgb value is a decimal created by dividing by 256 (b/c rgb values range from 0 - 255).
            rgb = list(colorsys.hls_to_rgb(hue, lightness, saturation))
            
            # To make each rgb value integers, we use this map.
            return list(map(lambda x : floor(x * 256), rgb))
            
    
    def __init__(self, saturation, lightness):
        """
        Create a new color shifter.
        
        @param {int} saturation : The HSL color saturation [0, 100].
        @param {int} lightness  : The HSL color lightness [0, 100].
        """
        self.color = ColorShifter.Color(0, saturation, lightness)
        self.minHue = 0
        self.maxHue = 360
        self.shiftType = "loop"
        self.increase = True
        
    def setHueRange(self, hueRange):
        """"
        Set the hue range that the HSL color cycles through.
        
        @param hueRange {list<int, int>} : The hue range. Properties include...
                                           - hueRange[0] == min hue value
                                           - hueRange[1] == max hue value
                                           - hueRange[0] <= hueRange[1]
                                           - hue values range : [0, 360]
        """
        if (len(hueRange) != 2):
            raise ValueError("hueRange must contain 2 elements: the min and max hue values.")
        
        if (hueRange[0] > hueRange[1]):
            raise ValueError("hueRange[0] must be <= hueRange[1]")
        
        MIN_HUE_VALUE = 0
        MAX_HUE_VALUE = 360
        if (hueRange[0] < MIN_HUE_VALUE):
            raise ValueError("hueRange[0] must be < {}".format(MIN_HUE_VALUE))
        if (hueRange[1] > MAX_HUE_VALUE):
            raise ValueError("hueRange[1] must be > {}".format(MAX_HUE_VALUE))
        
        self.minHue = hueRange[0]
        self.maxHue = hueRange[1]
        
    def setShiftType(self, shiftType):
        """
        Set the manner in which the HSL color hues shifts.
        
        @param {string} shiftType: Strings include...
                                   - "loop"   : Loop through hues.
                                   - "bounce" : Back and forth through hues.
        """
        self.shiftType = shiftType  
    
    def update(self):
        """
        Updates stored color.
        """
        hue = self.color.getHue()
        if (self.shiftType == "loop"):
            if (hue < self.maxHue):
                self.color.setHue(hue + 1)
            else:
                self.color.setHue(self.minHue)
                
        elif (self.shiftType == "bounce"):
            if (self.increase):
                if (hue < self.maxHue):
                    self.color.setHue(hue + 1)
                else:
                    self.increase = False
            
            else:
                if (hue > self.minHue):
                    self.color.setHue(hue - 1)
                else:
                    self.increase = True
    
    def getRGB(self):
        """
        @return {list<int, int, int>} : The current RGB color. Indicies include...
            - [0] : red value [0, 255]
            - [1] : green [0, 255]
            - [2] : blue [0, 255]
        """
        return self.color.getRGB()    
            
    def setSaturation(self, saturation):
        """
        Set the HSL color saturation.
        
        @param {int} saturation : HSL color saturation [0, 100].
        """
        self.color.setSaturation(saturation)
    
    def setLightness(self, lightness):
        """
        Set the HSL color lightness.
        
        @param {int} lightness : HSL color lightness [0, 100].
        """
        self.color.setLightness(lightness)
    
    
    
    