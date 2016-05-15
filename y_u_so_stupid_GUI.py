from pprint import pprint as pp #del me

try:
    from Tkinter import *
    from Tkinter.ttk import *
except ImportError:
    from tkinter import *
    from tkinter.ttk import *
    from tkinter import ttk as TTK

import time
import json
import y_u_so_stupid
from PIL import Image, ImageTk

def click_event(fun,pos):
    return lambda: fun(pos)

class TriviaGame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, padding="10 10 10 10")
        
        self.master = master #what's the purpose !?
        self.pack(fill=BOTH, expand=True)
        self.initGameWindow()
    
    def initGameWindow(self):
        #self.lbl = Label(self,text="...y u so stupid?")
        #self.lbl.grid(row=11,column=11)
        
        self.master.title("y u so stupid?")        
        self.quitButton = Button(self, text="Quit", command=self.exitGame)
        self.quitButton.grid(row=0,column=9, sticky=(N))

        self.startText = Label(self, text="Are you read?")
        self.startText.grid(row=0,column=0)

        self.question = Label(self, text="")
        self.correctAnswer = Label(self, text="")
        self.result = Label(self, text="")

        self.questionButtons = []
        
        self.startButton = Button(self, text="YES I AM", command=self.play)
        self.startButton.grid(row=1,column=1)

        self.nextQuestion = Button(self, text="Next question", command=self.generateQuestion)
        
        
    def clicked(self,event):
        if event.widget.choice == event.widget.answer:
            self.result = Label(self, text="CORRECT")
            self.correctAnswer = Label(self, text="u no stupid")
        else:
            self.result = Label(self, text="WRONG")
            txt = "y u so stupid..?\nAnwer: {0}".format(event.widget.answer)
            self.correctAnswer = Label(self, text=txt)
            

        
        
        self.result.grid(row=6,column=0)
        self.correctAnswer.grid(row=7,column=0)

        self.nextQuestion.grid(row=8,column=0)
            
    def play(self):
        self.startButton.grid_remove()
        self.startText.grid_remove()

        self.generateQuestion()
        

    def generateQuestion(self):
        if self.questionButtons:
            for b in self.questionButtons:
                b.grid_remove()
        self.nextQuestion.grid_remove()
        self.correctAnswer.grid_remove()
        self.result.grid_remove()
        question = json.loads(y_u_so_stupid.getRandomQuestion())
        self.question.grid_remove()
        self.question = Label(self, text=question['question'])
        self.question.grid(row=1,column=0)
        count = 2
        
        for c in question['choices']:
    
            b = TTK.Button(self,
                text=c,width=25)
            b.grid(row=count,column=0, ipadx=20, ipady=20,sticky=N)
            b.choice = c
            b.answer = question['answer']
            b.bind('<Button-1>', self.clicked)
            count += 1
            self.questionButtons.append(b)
            b.configure(background='black')
            
            print(self.winfo_geometry())
        
    def exitGame(self):
        
        exit()

root = Tk()
root.geometry("350x450")
app = TriviaGame(master=root)

app.mainloop()
