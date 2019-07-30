import asyncio
import time            
import pyaudio
import wave

class AudioRecorder():
    chunk         = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels      = 1
    fs            = 44100  # Record at 44100 samples per second
    
    def __init__(self, path):
        self.name = "Audio"
        self.audio = pyaudio.PyAudio()
        self.recording = False
        
        self.path = os.path.join(path, self.name)
        os.makedirs(self.path, exist_ok = True)

        
    def __del__(self):
        self.stopRecording()
        self.audio.terminate()
     
    def startRecording(self, period):
        if(self.recording) return
    
        self.stream = self.audio.open(
            format            = self.sample_format,
            channels          = self.channels,
            rate              = self.fs,
            frames_per_buffer = self.chunk,
            input             = True 
        )
        
        self.start_file_time = time.localtime()
        
        self.frames = []
        self.recording = True
        
    async def stopRecording(self):
        if( not self.recording ) return
    
        self.stream.stop_stream()
        self.stream.close()
        
        await self.saveAudio()

            
    async def main_loop(self):
        self.running = True 
        while(self.running):
        
            if(self.recording)::
                data = stream.read(chunk)
                frames.append(data)
                
                await asyncio.sleep( self.chunk / self.fs )  
            else:                    
                await asyncio.sleep( 1.0 / self.sample_rate )


    async def saveAudio(self):
    
        file_name = self.name + "_" + time.strftime("%Y%m%d-%H%M%S", self.start_file_time) + ".wav"
        
    
        filePath = os.path.join(self.path, file_name)
        
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
        
