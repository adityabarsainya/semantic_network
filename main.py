import os
import time
import knowledge_base as KB
import semantic_net as net
from tkinter import *
from tkinter import ttk
import webbrowser
from PIL import Image, ImageTk
import speech_recognition as sr
from pygame import mixer



start = time.time()


def close():
    global msg
    msg = entry1.get()
    root.destroy()


def buttonClick():

    mixer.init()
    mixer.music.load('to-the-point.mp3')
    mixer.music.play()

    r = sr.Recognizer()
    r.pause_threshold = 0.7
    r.energy_threshold = 400

    with sr.Microphone() as source:

        try:

            audio = r.listen(source, timeout=10)
            message = str(r.recognize_google(audio))

            entry1.focus()
            entry1.delete(0, END)
            entry1.insert(0, message)

        except sr.UnknownValueError:
            print('Google Speech Recognition could not understand audio')

        except sr.RequestError as e:
            print('Could not request results from Google Speech Recognition Service')

        except sr.WaitTimeoutError:
            print('Oops! Time out!')

        else:
            pass



root = Tk()
root.title('Voice recognizer')
style = ttk.Style()


image = Image.open('micro.png')
image = image.resize((30, 30), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)
label1 = ttk.Label(root, text='Query:',foreground='blue')
label1.grid(row=0, column=0)
entry1 = ttk.Entry(root, width=50)
entry1.grid(row=0, column=1, columnspan=4)
btn2 = StringVar()
MyButton2 = Button(root, image=photo, command=buttonClick, bd=0, activebackground='#c1bfbf', overrelief='groove', relief='sunken')
MyButton2.grid(row=0, column=5)
MyButton1 = ttk.Button(root, text='Quit', width=20, command=close)
MyButton1.grid(row=0, column=6)
entry1.focus()
root.wm_attributes('-topmost', 1)
btn2.set('google')
root.mainloop()


string=msg


#text to analyze
#string="""green kite was flying high"""
print(string)
string=string.lower()
relation={}


response=net.init(string)

net.word_info(response)

net.entailment(response)

relation=net.sentence_parse(response)

KB.knowledge_graph(relation)

end = time.time()
print("Time spent on execution: ",end - start)
print("Size of data base is: ",os.path.getsize("data.txt"))
