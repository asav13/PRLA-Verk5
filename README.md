# Y U so stupid - A Python Movie Trivia module

Reykjavík University, May 2016<br>
T-308-PRLA - The Python Programming Language<br>
Assignment nr 5<br>
Authors: asav13@ru.is, vedise13@ru.is

A Python module that generates random questions that can be used for Movie Trivia games.<br>
We couldn't decide weather to show its usage with a command line interface, website, or GUI client,
so we chose all :)


## Installation and dependencies

In order for everything to work properly you must have Python3 installed, and some pip packages:
-bs4
-tkinter
-Flask

```
	py -m pip install bs4
	py -m pip install tkinter
	py -m pip install Flask
```

### Use the module

#### As a module
```
import y_u_so_stupid
```
and call the method 
```
getRandomQuestion()
```

The method takes as a parameter the number of choices to return with the question, if no
parameter is specified the default number of choices is 4.

The methor returns a json object on the following form:

{
	"question": "Who was the director of La Haine?", 
	"answer": "Mathieu Kassovitz", 
	"choices": ["F.W. Murnau", "Mathieu Kassovitz", "John Lasseter", "Ingmar Bergman"]
}

You can use 
```
json.loads
``` 
to get it as a python dictionary type if preferred.

Simple example usage:
```
import y_u_so_stupid,json
...
...

question = json.loads(y_u_so_stupid.getRandomQuestion())	
print(question['question'])
for c in question['choices']:
	print(c)
answer = input()
if answer == question['answer']:
	print("Correct.")
else:
	print("Wrong.")

```

#### As a script
Run
```
py y_u_so_stupid.py 
```

##### More details:

usage: y_u_so_stupid.py [-h] [-q QUESTIONS] [-d {2,3,4,5,6,7,8,9,10}] [-k]

optional arguments:
  -h, --help            show this help message and exit
  -q QUESTIONS, --questions QUESTIONS
                        number of questions to return
  -d {2,3,4,5,6,7,8,9,10}, --difficulty {2,3,4,5,6,7,8,9,10}
                        difficulty,defined by number of choices
  -k, --keep-them-coming
                        continue getting questions until input is other than
                        y/Y


### The Clients

#### CLI - Command line interface
Either run
```
	py y_u_so_stupid_CLI.py
```
or double click the file and the game will start. This client takes the following optional arguments:
  -h, --help            show this help message and exit
  -q QUESTIONS, --questions QUESTIONS
                        number of questions to run
  -d {2,3,4,5,6,7,8,9,10}, --difficulty {2,3,4,5,6,7,8,9,10}
                        difficulty,defined by number of choices

#### WEBSITE
The website is currently being deployed at asabjork88.pythonanywhere.com

To run it locally you can also run
```
	py y_u_so_stupid_SERVER.py
```
or double click the file and then open 127.0.0.1:5000 in a browser

#### GUI  - Graphical User Interface
Either run
```
	py y_u_so_stupid_GUI.py
```
or double click the file and the game will open up.
