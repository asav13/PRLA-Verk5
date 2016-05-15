from pprint import pprint as pp #del me

try:
    from Tkinter import *
    from Tkinter.ttk import *
except ImportError:
    import tkinter as tk #for more config options
    #from tkinter import *
    #from tkinter.ttk import *
    from tkinter import ttk as TTK

import time
import json
import y_u_so_stupid
from PIL import Image, ImageTk

def click_event(fun,pos):
    return lambda: fun(pos)

class TriviaGame(tk.Frame):    
    def __init__(self, master=None, padding="10 10 10 10"):
        
        tk.Frame.__init__(self, master)
        self.configure(bg='black')
        self.pack(fill=tk.BOTH, expand=True)
        
        self.initGameWindow()

    def initGameWindow(self):

        self.master.title("y u so stupid?")        
        self.quitButton = tk.Button(self, text="Quit", command=self.exitGame)
        self.quitButton.configure(relief=tk.GROOVE,bg='black',fg='lightgray')
        self.quitButton.grid(row=0,column=9)

        self.startText = tk.Label(self, text="Are you read?")
        self.startText.configure(bg='black',fg='lightgray')
        self.startText.grid(row=0,column=0)

        self.question = tk.Label(self, text="")
        
        self.question.configure(bg='black',fg='lightgray')
        self.result = tk.Label(self, text="")
        self.result.configure(bg='black',fg='lightgray')

        self.questionButtons = []
        
        self.startButton = tk.Button(self, text="YES I AM", command=self.play)
        self.startButton.configure(relief=tk.GROOVE,bg='black',fg='lightgray')
        self.startButton.grid(row=1,column=1)

        self.nextQuestion = tk.Button(self, text="Next question", command=self.generateQuestion)
        
    def clicked(self,event):
        if event.widget.choice == event.widget.answer:
            self.result['text'] = "CORRECT\nu no stupid"
        else:
            self.result['text'] = "WRONG\ny u so stupid..?\nAnwer: {0}".format(event.widget.answer)
        
        self.result.grid(row=6,column=0)

        self.nextQuestion.grid(row=8,column=0)
            
    def play(self):
        self.startButton.grid_remove()
        self.startText.grid_remove()
        self.questionButtons = []
        for i in range(4):
            b = tk.Button(self,text="",width=25)
            b.grid(row=i+2,column=0, ipadx=20, ipady=20)
            b.configure(relief=tk.GROOVE,bg='black',fg='lightgray')
            b.bind('<Button-1>', self.clicked)
            self.questionButtons.append(b)
            
                
        self.nextQuestion.grid_remove()
        self.generateQuestion()
        

    def generateQuestion(self):

        self.result.grid_remove()
        question = json.loads(y_u_so_stupid.getRandomQuestion())
        self.question['text'] = question['question']
        self.question.grid(row=1,column=0)
        
        for i in range(4):
            self.questionButtons[i].choice = question['choices'][i]
            self.questionButtons[i]['text'] = question['choices'][i]
            self.questionButtons[i].answer = question['answer']
        
    def exitGame(self):
        
        exit()

root = tk.Tk()
root.configure(bd=10, bg='#CCFFFF')
#root.configure(bd=10, bg='#3C8B75')
root.geometry("350x450")

app = TriviaGame(master=root)
app.mainloop()
