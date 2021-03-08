from abc import abstractmethod, ABCMeta

class AmplitudeVisualizer(metaclass=ABCMeta):
    """
    An abstract class that's inherited by all amplitude based visualizers.
    """
    
    @abstractmethod
    def update(self, nextAvgAmp):
        """
        Updated the LED strip music visualilzer based on the provided
        "next" average amplitude data.
        
        @param {float} nextAvgAmp : The next average amplitude data.
        """
        pass
    
    @abstractmethod
    def turnOff(self):
        """
        Turns off the LED strip.
        """
        pass