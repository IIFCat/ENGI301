"""
--------------------------------------------------------------------------
Lighted Castle
--------------------------------------------------------------------------
License:   
Copyright 2018 <Sammi Lu>

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Use pyaudio to play music while led is shining
    user gets to choose between two different modes

"""

# ------------------------------------------------------------------------
# libs for several parts of the code
# ------------------------------------------------------------------------

# lib for music
import pyaudio
import wave

# lib for LED
import Adafruit_BBIO.GPIO as GPIO
import time

# lib for threading
import threading
from threading import Thread, Event
import time
import logging

# lib for freq
from pylab import*
from scipy.io import wavfile
import numpy as np

# lib for signal
import signal

# ------------------------------------------------------------------------
# define things
# ------------------------------------------------------------------------

# define LED
# Ping 1_2, 1_4 and 2_4 used for the three LEDs
GPIO.setup("P1_2", GPIO.OUT) #green
GPIO.setup("P1_4", GPIO.OUT) #red
GPIO.setup("P2_4", GPIO.OUT) #blue

# define stop event
stop_event = Event()

# ------------------------------------------------------------------------
# functions
# ------------------------------------------------------------------------

# function for getting the input from user
def get_user_input():
    print("Get User Input")
    
    try:
        
        modnum = float(input("  Mode Number                      : "))
        t_shut = float(input("  Shut Down Time                   : "))
        
        return (modnum,t_shut)
    except:
        print("\nInvalid Input")
        return(None, None)
        
# function for music playing, written as class for threading
class Mus(threading.Thread):
    # initialize the three variables
    chunk = None
    wf    = None
    p     = None
 
    def __init__(self):
        threading.Thread.__init__(self)
        # The shutdown_flag is a threading.Event object that
        # indicates whether the thread should be terminated.
        self.shutdown_flag = threading.Event()
 
        # define the three variables
        self.chunk = 1024
        self.wf = wave.open('CAGNET-+24-7+.wav', 'rb')
        self.p = pyaudio.PyAudio()
 
    def run(self):
 
        # check for stopping criteria
        while not self.shutdown_flag.is_set() and not stop_event.is_set():
            # open the music
            stream = self.p.open(
                format = self.p.get_format_from_width(self.wf.getsampwidth()),
                channels = self.wf.getnchannels(),
                rate = self.wf.getframerate(),
                output = True)
            data = self.wf.readframes(self.chunk)
            # check for stopping criteria
            while data != '' and not self.shutdown_flag.is_set() and not stop_event.is_set():
                # play the music
                stream.write(data)
                data = self.wf.readframes(self.chunk)

            # finish playing
            stream.close()
            time.sleep(0.5)
 
        # cleanup after stop playing
        self.p.terminate()
        
# function for shining the LED, written as class for threading
class Led(threading.Thread):
    # initialize the two variables
    pin = None
    dl  = None
 
    def __init__(self,pin,dl):
        threading.Thread.__init__(self)
        # The shutdown_flag is a threading.Event object that
        # indicates whether the thread should be terminated.
        self.shutdown_flag = threading.Event()
        
        # define the two variables
        self.pin = pin
        self.dl  = dl
 
    def run(self):
 
        # check for stopping criteria
        while not self.shutdown_flag.is_set() and not stop_event.is_set():
            # have the LED blink
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(self.dl)
            GPIO.output(self.pin, GPIO.LOW)
            time.sleep(self.dl)
            
# function for counting the time, written as class for threading
class Timing(threading.Thread):
 
    def __init__(self):
        threading.Thread.__init__(self)
        # The shutdown_flag is a threading.Event object that
        # indicates whether the thread should be terminated.
        self.shutdown_flag = threading.Event()
 
    def run(self):

        # initialize i for counting seconds
        i = 0
        
        # check for stopping criteria
        while not self.shutdown_flag.is_set() and not stop_event.is_set():
                # count up each time one second is passed
                i += 1
                time.sleep(1)
         
                # Here we make the check if the other thread sent a signal to stop execution.
                if stop_event.is_set():
                    break
                elif self.shutdown_flag.is_set():
                    break

# function for exit, written as class for threading
class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass
 
# function for exit, written as class for threading
def service_shutdown(signum, frame):
    #print("Trying to stop the Program")
    raise ServiceExit

# ------------------------------------------------------------------------
# main code
# ------------------------------------------------------------------------

if __name__ == "__main__":
    
    # Register the signal handlers
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    
    # Get user inputs
    # If you want to change the song, this is where you change it
    (modnum,t_shut) = get_user_input()
    sampFreq, snd = wavfile.read('CAGNET-+24-7+.wav')

    # getting delay of LED blinking from the song
    snd.dtype
    snd = snd / (2.**15)
    s1 = snd[:,0] 
    ind_pos = [0,1,2]
    (t_r, t_g, t_b) = s1[ind_pos]
    
    # start timing
    tim = Timing()
    tim.start()
    
    # adjust for mode 1
    if (modnum == 1):
        t_r = abs(t_r*5000)
        t_g = abs(t_g*5000)
        t_b = abs(t_b*5000)
        
        try:
            # start music
            t = Mus()
            t.start()
            
            # start blinking led
            lg = Led("P1_2", t_g)
            lr = Led("P1_4", t_r)
            lb = Led("P2_4", t_b)
            lg.start()
            lr.start()
            lb.start()
            
            # quit when time is up
            tim.join(timeout=t_shut)
            stop_event.set()
            quit()
            
        # or quit when asked to stop
        except ServiceExit:
            # Terminate the running threads.
            # Set the shutdown flag on each thread to trigger a clean shutdown of each thread.
            t.shutdown_flag.set()
            lg.shutdown_flag.set()
            lr.shutdown_flag.set()
            lb.shutdown_flag.set()
            tim.shutdown_flag.set()
            # Wait for the threads to close...
            t.join()
            lg.join()
            lr.join()
            lb.join()
            tim.join()
            
    # adjust for mode 2
    elif (modnum == 2):
        t_r = abs(t_r*50000)
        t_g = abs(t_g*50000)
        t_b = abs(t_b*50000)
        
        try:
            # start music
            t = Mus()
            t.start()
            
            # start blinking led
            lg = Led("P1_2", t_g)
            lr = Led("P1_4", t_r)
            lb = Led("P2_4", t_b)
            lg.start()
            lr.start()
            lb.start()
            
            # quit when time is up
            tim.join(timeout=t_shut)
            stop_event.set()
            quit()
            
        # or quit when asked to stop
        except ServiceExit:
            # Terminate the running threads.
            # Set the shutdown flag on each thread to trigger a clean shutdown of each thread.
            t.shutdown_flag.set()
            lg.shutdown_flag.set()
            lr.shutdown_flag.set()
            lb.shutdown_flag.set()
            tim.shutdown_flag.set()
            # Wait for the threads to close...
            t.join()
            lg.join()
            lr.join()
            lb.join()
            tim.join()
    # if not mode 1 or 2, give error message
    else:
        print("Mode Number Error. Please enter number 1 or number 2.")