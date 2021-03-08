import pyaudio
import wave
import sys
import math
import numpy
import socket
import struct
import time
import string
import json
import os
import random

from enum import Enum
from pip._internal import index


SERVER_IP   = "192.168.0.163" # Raspberry PI (wireless)
#SERVER_IP   = "192.168.0.13"  # Desktop
SERVER_PORT = 8523

class VisualizeType(Enum):
    """
    Specifies whether visualization should be done using the average
    amplitude of each audio chunk OR the frequency amplitudes of each audio
    chunk.
    """
    AMPLITUDE = 1
    FREQUENCY = 2

def getAvgAmp(wavData):
    """
    Takes byte data from a .wav file, then returns the average amplitude (in decibels [dB]) of that data.

    @param {bytes} : Byte data from a .wav file.

    @return {float}  : The average amplitude (in decibels [dB]) of the given bytes.
    """
    # wavDataInt should be int[]
    wavDataInt = numpy.frombuffer(wavData, dtype=numpy.int16) # convert bytes to int[]
        
    # Convert wavDataInt to an average amplitude (in decibels)
    linearRMS = numpy.sqrt(numpy.mean(list(d**2 for d in wavDataInt)))
    if (linearRMS == 0):
        return 0
    return 20 * math.log10(linearRMS) # decibels (dB) between 0dB -> -inf dB

# def getFFT_amp(wavData):
#     """
#     Gets the FFT amplitude data by calculating the FFT list, taking the absolute
#     value of each element in the FFT list, then returning the first half of the FFT list.
#     
#     @param {bytes}             : Byte data from a .wav file.
#     
#     @return {numpy.array_like} : A numpy array object with the amplitude data of each FFT value.
#                                  Each index represents a different frequency, equal to
#                                  index * (samplingRate / chunkSize)
#     """
#     # wavDataInt should be int[]
#     wavDataInt = numpy.frombuffer(wavData, dtype=numpy.int16) # convert byte array to an array of ints
#     
#     fft = numpy.fft.fft(wavDataInt)
#     fft_slice = fft[0:int(len(fft)/2)]    # We only need the 1st half of the FFT data
#     
#     
#     # Use this for amplitudes (in decibels)================
# #     for index in range(len(fft_slice)):
# #         complex_number = fft_slice[index]
# #          
# #         real = complex_number.real
# #         imaginary = complex_number.imag
# #         amplitude = 20*math.log10(math.sqrt(real**2 + imaginary**2)/len(fft))
# #         fft_slice[index] = amplitude
#     #=======================================================
#     
#     # Use this for values relative to the maximum=========
#     magnitudes = []
#     for index in range(len(fft_slice)):
#         complex_number = fft_slice[index]
#            
#         real = complex_number.real
#         imaginary = complex_number.imag
#         amplitude = math.sqrt(real**2 + imaginary**2)
#         magnitudes.append(amplitude)
#         
#     fft_slice = numpy.divide(magnitudes, max(magnitudes))
#     # ====================================================
#     
#     return fft_slice


# def getLargestN_FTTFreqAndAmp(wavData, n, samplingRate, chunkSize):
#     """
#     Returns a list of 2-tuples representing the top "n" frequencies in the
#     provided fft list (based on their amplitude). In each 2-tuple, the first element 
#     is the frequency and the second is its amplitude. The resulting list is sorted 
#     by the amplitude.
#     
#     @param {bytes} wavData    : Byte data from a .wav file.
#     @param {int} n            : The top "n" (frequency, amplitude) pairs to return.
#     @param {int} samplingRate : How many samples/sec (Hertz [Hz]) are used in the 
#                                 conversion from analog to digital.
#     @param {int} chunkSize    : The number of bytes of audio data to read in each iteration.
#     
#     @return {list<tuple<float, float>>} : The first element is the frequency & the second is the amplitude.
#     """
#     # Full FFT result, except all entries are swapped for their absolute value.
#     fft_amplitudes = getFFT_amp(wavData)
#     
#     # Get the indices of the n largest elements. Reverse the order so it's from greatest
#     # to least.
#     sortedIndices = numpy.argsort(fft_amplitudes)[-n:]
#     sortedIndices = numpy.flip(sortedIndices)
#     
#     # Create the list of 2-tuples
#     #    - Use the indices to calculate the corresponding frequency (index * (samplingRate / chunkSize))
#     #    - Use the value at fft_amplitudes[index] as the amplitude of the frequency
#     result = []
#     for index in sortedIndices:
#         frequency = index * (samplingRate / chunkSize)
#         result.append((frequency, fft_amplitudes[index]))
#         
#     return result


def wavFileScript(wavFile, visualizeType, connectionSocket):
    """
    Runs the music visualizer script for playing a .wav file. 
    
    @param {string} waveFile                : The location of the .wav file.
    @param {VisualizeType} visualizeType    : Specifies whether visualization should use the average amplitude of each
                                              audio chunk or the frequency amplitudes of each audio chunk.
    @param {socket.socket} connectionSocket  : A socket to send data to the music visualizer server.
    """
    try:
        wavRead = wave.open(wavFile, 'rb')     # Wave_read object
        CHUNK = 1536                           # The number of bytes of audio data to read in each iteration.
        SAMPLING_RATE = wavRead.getframerate() # How many samples/sec (Hertz [Hz]) are used in the conversion from analog to digital.
        p = pyaudio.PyAudio()                  # Used to play the audio.
        
        # format   : a PortAudio sample format (e.g. int16 [an integer w/ 16 bits]; int32; float 16; etc.)
        # channels : 1 for mono; 2 for stereo
        # rate     : sampling rate (how many samples/sec (Hertz [Hz]) are used in the conversion from analog to digital
        # output   : set to True b/c we're outputting audio (as opposed to inputting audio from a microphone)
        stream = p.open(format=p.get_format_from_width(wavRead.getsampwidth()),
                        channels=wavRead.getnchannels(),
                        rate=SAMPLING_RATE,
                        output=True)
        
        if (visualizeType == VisualizeType.AMPLITUDE):
            wavFileScriptAmplitude(wavRead, stream, CHUNK, connectionSocket)
        
#         elif (visualizeType == VisualizeType.FREQUENCY):
#             wavFileScriptFrequency(wavRead, stream, CHUNK)
        
        else:
            raise ValueError("Invalid VisualizeType given : {}".format(visualizeType))
            
    except Exception as e:
        print(string(e), file=sys.stderr)
        
    finally:
        # Close everything
        print("Stoping audio stream")
        stream.stop_stream()
        print("Closing audio stream")
        stream.close()
        print("Closing PyAudio")
        p.terminate()
        print("Closing wav_read")
        wavRead.close()
    
    
def sendAvgAmpData(avgAmp, connectionSocket):
    """
    Takes an average amplitude value, then sends it to the server via the provided
    socket.
    
    @param {float} avgAmp  : The average amplitude.
    @param {socket.socket} connectionSocket  : A socket to send data to the music visualizer server.
    """
    avgAmpBytes = struct.pack("f", avgAmp) # Convert the "avgAmp" float (16 bit = 4 Byte) object to a bytes object (also 4 Bytes)
    connectionSocket.sendall(avgAmpBytes)  # Send "avgAmpBytes"
    
    
def wavFileScriptAmplitude(wavRead, stream, chunkSize, connectionSocket):
    """
    A script for playing the .wav music visualizer with the average amplitude
    of each audio chunk.
    
    @param {wave.Wave_read} wavRead          : An object used to read chunks of byte data from the .wav file.
    @param {pyaudio.Stream} stream           : An object used to play the .wav file.
    @param {int} chunkSize                   : The number of bytes of audio data to read in each iteration.
    @param {socket.socket} connectionSocket  : A socket to send data to the music visualizer server.
    """           
    wavDataBytes = wavRead.readframes(chunkSize) # The next chunk of audio byte data.
    chunkNumber = 0                              # Keep track of the number of iterations (i.e. number of chunks)
    
    # Play the audio
    while wavDataBytes != b'':        
        avgAmp = getAvgAmp(wavDataBytes)     
        sendAvgAmpData(avgAmp, connectionSocket)
        
        # Write the current "chunk" of audio to the
        # audio output stream
        stream.write(wavDataBytes)
        
        # Visualize the amplitude data
        #
        # Column 1 : The chunk number
        # Column 2 : The average amplitude of this chunk
        # Column 3 : A horizontal bar representing the amplitude size
        bars="#"*int(avgAmp)
        print("{:05d} {:05f} {}".format(chunkNumber, avgAmp, bars))
        
        # Get the next "chunk" of audio (stored as
        # a bytes object).
        wavDataBytes = wavRead.readframes(chunkSize)
        
        chunkNumber += 1 # Update the chunk number
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# def wavFileScriptFrequency(wavRead, stream, chunkSize):
#     """
#     A script for playing the .wav music visualizer with the frequency amplitudes
#     of each audio chunk.
#     """
#     SAMPLING_RATE = wavRead.getframerate() # How many samples/sec (Hertz [Hz]) are used in the conversion from analog to digital.
#     
#     # Contains the next "chunk" bytes of audio (stored as
#     # a bytes object).
#     wavDataBytes = wavRead.readframes(chunkSize)
#     
#     chunkNumber = 0 # Keep track of the number of iterations (i.e. number of chunks)
#     # Play the audio
#     while wavDataBytes != b'':
#         
#         # Write the current "chunk" of audio to the
#         # audio output stream
#         stream.write(wavDataBytes)
#         
#         largest_10_freq = getLargestN_FTTFreqAndAmp(wavDataBytes, 10, SAMPLING_RATE, chunkSize)
#         
#         print("{:05d} {}".format(chunkNumber, largest_10_freq))
#         
#         # Get the next "chunk" of audio (stored as
#         # a bytes object)
#         wavDataBytes = wavRead.readframes(chunkSize)
#         
#         chunkNumber += 1 # Update the chunk number
#     
#     
# 
# def recordingScript():
#     CHUNK = 1024 # The number of bytes of audio data to read next.
#     RATE = 44100 # Recording frequency (i.e. # samples / sec.)
# 
#     p = pyaudio.PyAudio()
#     stream = p.open(format=pyaudio.paInt16,
#                     channels=1,
#                     rate=RATE,
#                     input=True,
#                     frames_per_buffer=CHUNK)
# 
#     for i in range(int(10*RATE/1024)):
#         data = numpy.frombuffer(stream.read(CHUNK), dtype=numpy.int16) # convert byte array to an array of ints
# 
#         avgAMP=getAvgAmp(data)
#         bars="#"*int(avgAMP)
#         
#         fft_slice = numpy.abs(numpy.fft.fft(data)[0:int(CHUNK/2)])
#         print("{:05d} {:05f} {}".format(i, avgAMP, bars))
# 
#         
#     stream.stop_stream()
#     stream.close()
#     p.terminate()
# 


def getJsonData(jsonFile):
    """
    @param {string} jsonFile : Location of JSON file.
    
    @return {dict} : A dictionary representing the JSON file.
    """
    data = dict()
    with open(jsonFile) as file:
        data = json.load(file)
        
    return data

def sendDictData(dictData, connectionSocket):
    """
    Sends a dictionary to a server as a JSON file.
    
    @param {dict} dictData : A dictionary.
    @param {socket.socket} connectionSocket : The socekt used to send data to the server.
    """
    jsonDataBytes = json.dumps(dictData).encode("utf-8")
    connectionSocket.sendall(jsonDataBytes)

if __name__ == "__main__":

    # There must be 2 argument on the command line:
    #    1st : A .wav file (to play a singular song) or a directory of .wav files (to play multiple songs; non-.wav files are ignored).
    #    2nd : A .json config file (used by the server to configure the LED lights).
    if (len(sys.argv) != 3):
        raise ValueError("Please provide a .wav file or a directory of .wav files as the 1st argument on the command line and a .json config file as the 2nd argument.")
        time.sleep(5)
    
    wavPath = sys.argv[1]
    jsonPath = sys.argv[2]

    # Check if the first argument is a valid .wav file or directory. ========================================================
    playlist = [] # If the wavPath is a directory of .wav files, we will store the names of each .wav files here.
    
    if (os.path.isfile(wavPath) and wavPath.lower().endswith(".wav")):
        playlist.append(wavPath)
    elif (os.path.isdir(wavPath)):
        # Add the filename of each .wav file to "playlist"
        for entry in os.scandir(wavPath):            
            if (entry.is_file() and entry.name.lower().endswith(".wav")):
                playlist.append(entry.path)     
    else:
        raise ValueError("Please provide a .wav file or a directory of .wav files as the 1st argument on the command line.")
        time.sleep(5)
    
    random.shuffle(playlist)
    # =======================================================================================================================
    
    # Read the JSON file and store it as a dict<str, str>.
    jsonData = getJsonData(jsonPath)
    
    index = 0
    while True:
        try:
            # We've reached the end of the playlist. Go back to the start.
            if (index >= len(playlist)):
                index = 0
                
            # Get the next .wav file and update the index.
            wavFile = playlist[index]
            index += 1
            print("Playing song : {}".format(wavFile))
            time.sleep(3)

            # AF_INET     : Use IPv4
            # SOCK_STREAM : Use TCP (all packets arrive in the order they were sent)
            connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connectionSocket.connect((SERVER_IP, SERVER_PORT))
            
            # Send the JSON configuration file.
            sendDictData(jsonData, connectionSocket)
            
            # Wait for the server to say it's done configuring based on the JSON file we sent.
            BUFF_SIZE = 1024
            serverResponse = b'0'
            while (serverResponse != b'1'):
                serverResponse = connectionSocket.recv(BUFF_SIZE)
            
            # Start the music. Send avg. amp data to server so it can light up the LEDs.
            wavFileScript(wavFile, VisualizeType.AMPLITUDE, connectionSocket)
            
            # Wait for the server to say it is done.
#             serverResponse = b'0'
#             while (serverResponse != b'1'):
#                 serverResponse = connectionSocket.recv(BUFF_SIZE)

        except KeyboardInterrupt as e: # Temporary : Skip to next song
            print("Keyboard interrupt detected. Skipping to next song...")
            continue
        
        except Exception as e: # Any other exception will end the program.
            print(e, file=sys.stderr)
            print("Closing connection")
            connectionSocket.close()
            break
        
        finally: # Go to the next song.
            print("Closing connection")
            connectionSocket.close()     
            print("Playing next song...")
    
    
