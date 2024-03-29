import asyncio
from datetime import datetime          
import pyaudio
import wave
import os

import RPi.GPIO as GPIO

from src.Writer import Writer

AUDIO_BUTTON_GPIO = 12

class AudioRecorder():
    chunk         = 4096  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels      = 1
    fs            = 44100  # Record at 44100 samples per second
    input_device  = 1

    file_split_time = 30
    max_record_time = 7600
 
    def __init__(self, writer):
        self.name = "Audio"
        self.audio = pyaudio.PyAudio()
        self.recording = False
        
        self.writer = writer
        

        self.path = os.path.join(self.writer.path, self.name)
        os.makedirs(self.path, exist_ok = True)

        assert(GPIO.getmode() == GPIO.BCM )

        GPIO.setup(AUDIO_BUTTON_GPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP)

        self.lastButtonDown = self.buttonDown = self.isButtonDown()

    def isButtonDown(self):
        return not GPIO.input(AUDIO_BUTTON_GPIO)

    def get_status_messages(self):
        return [("/{}/recording/".format(self.name), self.recording)]
        
    def __del__(self):
        self.audio.terminate()
     
    async def timer(self, time):
        await asyncio.sleep(time)
        return

    async def setTimer(self, timer, callback):
        await timer
        await callback


    async def startRecording(self, period=None):
        if(self.recording) : return
        print("Starting recording")
        self.stream = self.audio.open(
            format             = self.sample_format,
            channels           = self.channels,
            rate               = self.fs,
            frames_per_buffer  = self.chunk,
            input_device_index = self.input_device,
            input              = True
        )
        
        self.start_file_time = datetime.now()
        self.start_time = self.start_file_time
        self.frames = []
        
        if(self.stream.is_active()):
            self.recording = True
        else:
            print("Stream not active")

        if(period is not None):
            period = min(period, max_record_time)
            await self.setTimer( self.timer(period), self.stopRecording())

        
        
    async def stopRecording(self):
        if( not self.recording ) : return
        self.recording = False
        self.stream.stop_stream()
        self.stream.close()
        print("Recording Stopped")
        await self.saveAudio()

        
    async def main_loop(self):
        self.running = True

        await self.startRecording()
 
        while(self.running):
       
            if(self.recording ):
                data = self.stream.read(self.chunk, exception_on_overflow = False)
                self.frames.append(data)
                
                record_time = (datetime.now() - self.start_time).seconds
                file_time   = (datetime.now() - self.start_file_time).seconds
                
                if(record_time > self.max_record_time):
                    self.stopRecording()
                elif( file_time > self.file_split_time ):
                    self.start_file_time = datetime.now()
                    await self.saveAudio()

                await asyncio.sleep( 0 )  
            else:                    
                await asyncio.sleep( 0 )


    async def saveAudio(self):

        file_name = "{}_{}.wav".format(self.name, self.start_file_time.strftime("%Y%m%d-%H%M%S"))

        if(not self.writer._valid_to_write() ):
            print("Volume not valid for writing")
            return

        filePath = os.path.join(self.path, file_name)
        
        print("Saving Audio {}".format(filePath))
        
        wf = wave.open(filePath, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        
