import json
import y_u_so_stupid
try:
    import Tkinter as tk
    from Tkinter import ttk as ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk as ttk

def click_event(fun,pos):
    return lambda: fun(pos)

class TriviaGame(tk.Frame):    
    def __init__(self, master=None):
        
        tk.Frame.__init__(self, master,padx=15)
        self.configure(bg='black')
        self.pack(fill=tk.BOTH, expand=True)
        
        self.initGameWindow()

    def initGameWindow(self):
        self.questionButtons    = []
        self.score              = 0
        self.highscore          = 0
        self.master.title("y u so stupid?")
        
        self.quitButton = tk.Button(self, text="Quit", command=self.exitGame)
        self.quitButton.configure(relief=tk.GROOVE,bg='black',fg='lightgray')
        self.quitButton.grid(row=0,column=0,sticky=tk.E)

        self.question = tk.Label(self, text="Are you ready !?\n Or are U stupid?")
        self.question.configure(bg='black', fg='lightgray',wraplength=200, font="Cambria 13 bold")
        self.question.grid(row=1,column=0)
        
        self.result = tk.Label(self, text="")
        self.result.grid(row=6,column=0)
        self.result.configure(bg='black',fg='lightgray', font="Cambria",pady=8)

        startingTexts = ["YES I AM","No wait..", "...uuuhhh","YOU ARE"]
        for i in range(4):
            self.startButton = tk.Button(self, text=startingTexts[i], command=self.play,width=20)   
            self.startButton.configure(relief=tk.GROOVE,bg='black',fg='lightgray')
            self.startButton.grid(row=i+2,column=0,padx=50,pady=5,ipadx=20, ipady=10)
            
        self.nextQuestion = tk.Button(self, text="Next question", command=self.generateQuestion)
        self.nextQuestion.configure(bg='black', fg='lightgray',wraplength=200, font="Cambria")

        self.retryButton = tk.Button(self, text="Nooooo! One more round!", command=self.generateQuestion,width=20)   
        self.retryButton.configure(relief=tk.GROOVE,bg='black',fg='lightgray', font="Cambria")
        
    def clicked(self,event):
        
        for b in self.questionButtons:
            if b.answer == b.choice:
                b.configure(fg='green')
            elif b == event.widget and b.answer != b.choice:
                b.configure(fg='red')
            else:
                b.configure(fg='grey')
            b.unbind('<Button-1>')

        if event.widget.choice == event.widget.answer:
            self.score += 10
            self.result['text'] = "CORRECT\nu no stupid\nScore: {0}".format(self.score)
            self.nextQuestion.grid(row=8,column=0)
        else:
            self.highscore = max(self.score,self.highscore)
            self.result['text'] = "GAME OVER\ny u so stupid..?\nScore: {0}\nHighscore: {1}".format(self.score, self.highscore)
            self.score = 0
            self.retryButton.grid(row=8,column=0,ipady=4, ipadx=4)
        
            
    def play(self):
        self.startButton.grid_remove()
        for i in range(4):
            b = tk.Button(self,text="",width=20)
            b.grid(row=i+2,column=0, padx=50,pady=5,ipadx=10, ipady=10)
            b.configure(relief=tk.GROOVE,bg='black',fg='lightgray', font="Cambria 12 bold")
            b.bind('<Button-1>', self.clicked)
            self.questionButtons.append(b)
            
        self.generateQuestion()
        
    def generateQuestion(self):
        self.result['text'] = "\n\nScore: {0}".format(self.score)
        self.retryButton.grid_forget()
        self.nextQuestion.grid_forget()

        question                = json.loads(y_u_so_stupid.getRandomQuestion())
        self.question['text']   = question['question']
        
        
        for i in range(4):
            self.questionButtons[i].choice      = question['choices'][i]
            self.questionButtons[i]['text']     = question['choices'][i]
            self.questionButtons[i].answer      = question['answer']
            self.questionButtons[i].bind('<Button-1>', self.clicked)
            self.questionButtons[i].configure(fg='lightgray')
        
    def exitGame(self):
        exit()
        
        

root = tk.Tk()
root.configure(bd=10, bg='#CCFFFF')
root.geometry("350x520")

app = TriviaGame(master=root)
app.mainloop()
