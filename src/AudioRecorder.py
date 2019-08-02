import asyncio
import datetime            
import pyaudio
import wave
import os

class AudioRecorder():
    chunk         = 4096  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels      = 1
    fs            = 44100  # Record at 44100 samples per second
    input_device  = 1

    
    def __init__(self, writer):
        self.name = "Audio"
        self.audio = pyaudio.PyAudio()
        self.recording = False
        
        self.writer = writer
        
        if(not self.writer._valid_to_write() ):
            print("Volume not valid for writing")
            return
            
        self.path = os.path.join(self.writer.path, self.name)
        os.makedirs(self.writer.path, exist_ok = True)

        
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
    
        self.stream = self.audio.open(
            format             = self.sample_format,
            channels           = self.channels,
            rate               = self.fs,
            frames_per_buffer  = self.chunk,
            input_device_index = self.input_device,
            input              = True
        )
        
        self.start_file_time = datetime.now()
        
        self.frames = []
        
        if(self.stream.is_active()):
            self.recording = True
        else:
            print("Stream not active")

        if(period is not None):
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
        while(self.running):
        
            if(self.recording ):
                data = self.stream.read(self.chunk, exception_on_overflow = False)
                self.frames.append(data)
                
                await asyncio.sleep( 0 )  
            else:                    
                await asyncio.sleep( 0.5 )


    async def saveAudio(self):
        print("Saving Audio")
        file_name = self.name + "_" + self.start_file_time.strftime("%Y%m%d-%H%M%S") + ".wav"
        
    
        filePath = os.path.join(self.writer.path, file_name)
        
        wf = wave.open(filePath, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        
