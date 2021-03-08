import socket
import struct
import time
import json
import sys
from center_double_bar_visualizer import CenterDoubleBarVisualizer

ACCEPTED_CLIENT_IP = ""               # Empty string : Any local IP is acceptable
#ACCEPTED_CLIENT_IP = "127.0.0.1"     # (i.e. localhost) : Only clients on this computer are allowed to connect to this server
LISTENING_PORT = 8523                 # What port this server listens at

SERVER_SOCKET_DEADLINE = 300.0        # How many seconds the server socket will wait for a client to connect until it closes.
CONNECTION_SOCKET_DEADLINE = 1.0      # How many seconds the connection socket will wait for new data until it closes.

# ===============================================================================================================================================================
PIN_NUMBER = 21        # This is the GPIO number, not the board pin number (i.e. GPIO.BCM, not GPIO.BOARD)
NUMBER_OF_LEDS = 300   # The total number of LEDS
BRIGHTNESS = 0.05      # A value between 0.0 to 1.0 determines the brightness of all LEDs
# =============================================================================================================================

def receiveJsonConfig(connectionSocket):    
    """
    Get the JSON configuration file.
    
    @param {socket.socket} connectionSocket : The socket that the client uses to pass
                                              data to this server.
                                              
    @return {dict<str,str>} : A dictionary representing the JSON file.
    """
    jsonDataBytes = connectionSocket.recv(1024)
    return json.loads(jsonDataBytes.decode('utf-8'))

def configureVisualizer(visualizer, jsonData):
    """
    Configures the provided center double bar visualizer based on the provided JSON config file.
    
    @param {CenterDoubleBarVisualizer} visualizer          : The visualizer.
    @param {dict<str,str>}             jsonData            : A dictionary representing the JSON config file.
    """
    visualizer.setAmpThreshold(int(jsonData["ampThreshold"]))
    visualizer.setLEDPerAmp(float(jsonData["ledPerAmp"]))
    visualizer.setBrightness(float(jsonData["brightness"]))
    visualizer.setSaturation(int(jsonData["saturation"]))
    visualizer.setLightness(int(jsonData["lightness"]))
    
    hueRange = [int(jsonData["hueRange"][0]), int(jsonData["hueRange"][1])]
    visualizer.setHueRange(hueRange)
    visualizer.setShiftType(jsonData["colorChangeType"])
    

if __name__ == "__main__":        
    # AF_INET     : Use IPv4
    # SOCK_STREAM : Use TCP (all packets arrive in the order they were sent)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        try :                         
            serverSocket.settimeout(SERVER_SOCKET_DEADLINE)
            serverSocket.bind((ACCEPTED_CLIENT_IP, LISTENING_PORT))        # This server will accept clients whose IP is "ACCEPTED_CLIENT_IP". This server will listen on port LISTENING_PORT
            serverSocket.listen()                                          # Tell the socket that it's a "listening" socket. It will listen at its bound port for any messages from its bound IP address
            
            visualizer = CenterDoubleBarVisualizer(PIN_NUMBER, NUMBER_OF_LEDS, BRIGHTNESS)
            
            while True:
                print("Waiting for client to connect...")
                connectionSocket, clientIpAndPort = serverSocket.accept()  # Block & wait for an incoming connection. When a client connects, returns a socket object (representing the connection) and a 2-tuple w/ the client socket's IP and port
                print("Connected by IP ({}) using port ({})".format(clientIpAndPort[0], clientIpAndPort[1]))
                
                try: 
                    chunkNumber = 0
                    with connectionSocket:                        
                        # First, get the configuration data
                        print("receiving json config")
                        jsonData = receiveJsonConfig(connectionSocket)
                        print("using configuration: {}".format(jsonData))
                        
                        # Next, create the LED visualizer
                        # ================================================================================================== 
                        configureVisualizer(visualizer, jsonData)                              
                        print("configuration complete!")
                        # ==================================================================================================
                        
                        # Tell the client we're done configurating
                        connectionSocket.sendall(b'1')
                        
                        # We can't use a socket.socket.timeout() for the connection socket. Instead, we use time.time() to compare the current
                        # time to when the "deadline" is.
                        deadline = time.time() + CONNECTION_SOCKET_DEADLINE
                        print("starting music visualization")
                        while True:
                            # Read 4 Bytes of data sent by the client
                            byteData = connectionSocket.recv(4)
                            if (byteData == b''):
                                if (time.time() >= deadline):
                                    print("Connection socket timed out. Turning off LEDs.")
                                    # ==========================================================================================
                                    print("Turning off LEDs")
                                    visualizer.turnOff()
                                    # ==========================================================================================
                                    break
                                chunkNumber = 0
                                continue
                            
                            deadline = time.time() + CONNECTION_SOCKET_DEADLINE # Reset deadline
                             
                            # Those 4 Bytes of data should be a floating point number describing the avg. amplitude of the audio chunk.
                            [nextAvgAmp] = struct.unpack("f", byteData)
                             
#                             print("{:05d} {:05f}".format(chunkNumber, nextAvgAmp))
                             
                            # =========================================================================================================================
                            visualizer.update(nextAvgAmp)
                            # =========================================================================================================================
                             
                            chunkNumber += 1
                        print("Music visualization complete!")
                             
                except KeyboardInterrupt as e:
                    print("Keyboarad interrupt. Exiting application")
                    print("Turning off LEDs")
                    visualizer.turnOff()
                    print("Closing connection socket.")
                    raise e
                
                # The client closed their application.
                except ConnectionResetError as e:
                    print(e, file=sys.stderr)
                    print("Turning off LEDs")
                    visualizer.turnOff()
                    print("Closing connection")
                             
        except socket.timeout as e:
            print("Server socket timed out. Exiting application.")
            print("Turning off LEDs")
            visualizer.turnOff()
            print("Closing server socket.")
            
         
        except KeyboardInterrupt as e: 
            print("Turning off LEDs")
            visualizer.turnOff()
            print("Closing server socket.")
            
            
        
             
             
            
        
