import pyaudio 
import wave
import speech_recognition as sr

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
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
    print("Grabación terminada")
    menu(output_file)
    
def play(output_file):# The size of the buffer.
    CHUNK = 1024
    with wave.open(output_file,'rb') as wf:
        p= pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(), rate = wf.getframerate(),output=True)  
        data = wf.readframes(CHUNK)
        while(len(data)>0):
            stream.write(data)
            data = wf.readframes(CHUNK)
        stream.close()
        p.terminate()
    toText(output_file)
    
def toText(output_file):
    print("In process")
    r = sr.Recognizer()
    with sr.AudioFile(output_file) as source:
        audio = r.record(source)
    try:
        texto = r.recognize_google(audio, language="es-CO")
        print(texto)
    except sr.UnknownError:
        print("Google no entendió el audio")
    except sr.RequestError as e:
        print("Error de conexión a Google service; {0}".format(e))

  
def menu(output_file):
    x = int(input("Quieres reproducir tu grabacion? (1:Si 0:No)"))
    if(x ==1):
        play(output_file)
    elif(x ==0):
        toText(output_file)
    else:
        print("Ingrese una opcion valida")
        menu(output_file)
        
def welcome():
    output_file = input("Ingrese el nombre del archivo para guardar la grabacion ")
    print("Input:" + output_file)
    time = input("Ingrese el tiempo que desea grabar (Segundos) ")
    print("Input:" + time)
    time = int(time)
    record(time, output_file) 
           
    
if __name__ == "__main__":
    welcome()
