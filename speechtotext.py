import pyaudio 
import wave

def record(time, output_file):
    ##Parameters for pyaudio
    chunk = 1024 #Size in bytes
    format = pyaudio.paInt16 #
    channels = 1 #2 = stereo, 1=mono
    rate = 44100 #Sampling frequency
    record_seconds = time
    #Initialize pyaudio
    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=rate,input=True, frames_per_buffer=chunk)
    print('Grabando...')
    frames = []
    for i in range(0, int(rate / chunk * time)):
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    with wave.open(output_file,'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_rate(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
    
def welcome():
    output_file = input("Ingrese el nombre del archivo para guardar la grabacion")
    print("Input:" + output_file)
    time = input("Ingrese el tiempo que desea grabar (Segundos)")
    print("Input:" + time)        
    
if __name__ == "__main__":
    welcome()
