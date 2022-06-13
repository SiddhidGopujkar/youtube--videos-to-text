from argparse import FileType
from tkinter import E
import PySimpleGUI as sg
import moviepy.editor as mp
import os
import speech_recognition as sr 
import _thread
import time

def myFunc(e):
    return len(e)

def prs(i,end,video,wav_path):
    clip = mp.VideoFileClip(video).subclip(i,end)
    string = 'converted_audio_{}.wav'.format(i)
    string_1 = wav_path +'\\'+ string
    clip.audio.write_audiofile(string_1)

def convert_wavs(t_d,total_duration,video,wav_path):
    for i in range(0,total_duration,60):
        if((t_d - i) <60):
            print("subclip({},{})".format(i,t_d))
            _thread.start_new_thread( prs, (i,t_d,video,wav_path,))
        else:
            print("subclip({},{})".format(i,i+60))
            _thread.start_new_thread( prs, (i,i+60,video,wav_path,))  

def convert_txts(wavs, wav_path, txt_path):
    for wav in wavs:
      _thread.start_new_thread( start_convert, (wav,wav_path,txt_path,))

def start_convert(wav,wav_path, txt_path):
    
    string_2 = wav_path+'\\'+wav
    print(string_2)
    audio = sr.AudioFile(string_2)
    r = sr.Recognizer()
    with audio as source:
        audio_file = r.record(source)
    result = r.recognize_google(audio_file)
    strdest = txt_path+'\\'+wav[:-4]
    print(wav)
    with open(strdest+'.txt',mode ='w') as file:
        file.write(result+"            ")
        file.close()

def gui():
    sg.theme('LightBrown1')
    layout = [[sg.T("")], [sg.T("")], [sg.Text("Choose a video file: "), sg.Input(), sg.FileBrowse(key="-IN-")],
            [[sg.T("")], [sg.T("")], sg.Button("Next", key="b1")]  
            ]
    window = sg.Window('Page 1', layout, size=(600, 200))
    while True:
        event, values = window.read()
        video = values["-IN-"]
        print("video name is "+video)

        if event == sg.WIN_CLOSED or event=="Exit":
            break
        elif event == "b1":

            layout1 = [
                    [sg.Text("Choose a folder to store audio files: ")],
                    [sg.Input(key="-IN2-" ,change_submits=True), sg.FolderBrowse(key="-IN-")],
                    [sg.Button("convert from video to audio")],
                    [sg.Button("View result")],
                    [sg.Text('Files')],
                    [sg.Multiline(key='files', size=(60,30), autoscroll=True)],
                    [sg.Button('Convert from audio to text')] ]

            window = sg.Window('Test', layout1)

            while True:
                event, values = window.read()
                wav_path = values["-IN2-"]
                # print(event)
                if event is None or event == 'Exit':
                    window.close()
                    break

                if event == 'convert from video to audio' :
                    sg.Popup('Converting...This Might take a while...Click On View result button to see the audio files', keep_on_top=True, background_color='white', text_color='Red')
                    global total_duration
                    t_d = mp.VideoFileClip(video).duration
                    print(t_d)
                    total_duration = int(t_d) 
                    convert_wavs(t_d, total_duration,video,wav_path)
                    time.sleep(20)
                    
                elif event == "View result":
                    filenames = os.listdir(wav_path)
                    filenames.sort(key = myFunc)
                    window['files'].update("\n".join(filenames))
                    sg.Popup('Audio files converted !! ', keep_on_top=True)
                
                elif event == "Convert from audio to text":
                    layout2 = [
                    [sg.Text("Choose a folder to store .txt files: ")],
                    [sg.Input(key="-IN3-" ,change_submits=True), sg.FolderBrowse(key="-IN-")],
                    [sg.Button("GO")],
                    [sg.Button("View result")],
                    [sg.Text('txt Files')],
                    [sg.Multiline(key='txt files', size=(60,30), autoscroll=True)],
                    ]

                    window2 = sg.Window('Final', layout2)
                    while True:
                        event, values = window2.read()
                        txt_path = values["-IN3-"]

                        if event is None or event == 'Exit':
                            window.close()
                            break

                        elif event == "GO":
                            sg.Popup('Converting...This Might take a while...Click On View result button to see the .txt files', keep_on_top=True, background_color='white', text_color='Red')
                            txt_path = values["-IN3-"]
                            wavs = os.listdir(wav_path)
                            wavs.sort(key = myFunc)
                            # print(wavs)
                            convert_txts(wavs, wav_path, txt_path)
                            time.sleep(20)
                        
                        elif event == "View result":
                            filenames = os.listdir(txt_path)
                            filenames.sort(key = myFunc)
                            window2['txt files'].update("\n".join(filenames))
                            sg.popup("All files generated!...Starting merging", keep_on_top=True,background_color='white', text_color='Red')
                            time.sleep(5)

                            for t in filenames:
                                with open(txt_path+'\\'+t,mode ='r') as file:
                            #         print(file.read())
                                    text = file.read()
                            #         print(text)
                                    with open(txt_path+'\\'+'final.txt', mode = 'a') as f:
                                        f.write(text)        
                            sg.popup("Yay..!! Merged text file is final.txt", keep_on_top=True,background_color='white', text_color='Red')


if __name__ == "__main__":
    try:
        gui()
        print("Completed!")
    except:
        print()