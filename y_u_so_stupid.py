from pprint import pprint
import requests; 
import os
import sys
from bs4 import BeautifulSoup as BS
from random import choice
import sys

DATA            = r"C:\Users\asabj\Dropbox\Skúl\PRLA\Verkefni\PRLA-Verk5\data.txt"
ACTORS          = r"C:\Users\asabj\Dropbox\Skúl\PRLA\Verkefni\PRLA-Verk5\actors.txt"
DIRECTORS       = r"C:\Users\asabj\Dropbox\Skúl\PRLA\Verkefni\PRLA-Verk5\directors.txt"
IMDB_LIST       = r"http://www.imdb.com/chart/top?ref_=nv_mv_250_6"
IMDB_BASE_URL   = r"http://www.imdb.com"

movies      = []
actors      = []
directors   = []
player = {}

def getActorsBase():
    actors = set()
    
    for m in movies:
        for a in getActors(m['link']):
            actors.add(a)
        if len(actors) >= 100:
            break
        
    return list(actors)

def getDirectorsBase():
    directors = set()
    
    for m in movies:
        directors.add(getDirector(m['link']))
        if len(directors) >= 100:
            break
        
    return list(directors)

def init():
    global movies
    global actors
    global directors
    global player

    try:
        file    = open(DATA)
        movies  = eval(file.read())
        file.close()
    except FileNotFoundError:
        file    = open(DATA, 'w')
        movies  = getMovies()
        file.write(str(movies))
        file.close()

    try:
        file    = open(ACTORS)
        actors  = list(eval(file.read()))
    except FileNotFoundError:
        file    = open(ACTORS, 'w')
        actors  = getActorsBase()
        file.write(str(actors))
        file.close()

    try:
        file        = open(DIRECTORS)
        directors   = list(eval(file.read()))
    except FileNotFoundError:
        file        = open(DIRECTORS, 'w')
        directors   = getDirectorsBase()
        file.write(str(directors))
        file.close()
    
    
    player['nr']    = 1
    player['score'] = 0




def getMovies():
    response    = requests.get(IMDB_LIST, headers = {'accept-language': 'en-US, en'})
    text        = response.text
    soup        = BS(text, 'html.parser')
    movieList   = []
    
    for line in soup.findAll('td', {"class": "titleColumn"}):
        m = dict()
        m['link']       = IMDB_BASE_URL + line.find('a').attrs['href']
        m['title']      = line.find('a').text
        m['year']       = (line.find('span').text)[1:-1]
        #m['actors'],m['director']     = getActorsAndDirector(m['link'])
        #m['director']   = getDirector(m['link'])
        
        movieList.append(m)

    return movieList

def getActorsAndDirector(link):
    text    = requests.get(link).text
    soup    = BS(text, 'html.parser')
    actors  = []

    for line in soup.findAll('span', {"itemprop": "actors"}):
        name = line.find('span',{"itemprop":"name"}).text
        actors.append(name)
        
    director = (soup.find('span', {"itemprop": "director"})).find('span', {"itemprop":"name"}).text
    return actors,director

def getActors(link):
    text    = requests.get(link).text
    soup    = BS(text, 'html.parser')
    actors  = []

    for line in soup.findAll('span', {"itemprop": "actors"}):
        name = line.find('span',{"itemprop":"name"}).text
        actors.append(name)
        
    return actors

def getDirector(link):
    text    = requests.get(link).text
    soup    = BS(text, 'html.parser')

    return (soup.find('span', {"itemprop": "director"})).find('span', {"itemprop":"name"}).text

def randomQuestion():
    movie = choice(movies)

    q = choice(['a','d','y','a','d','y','a','d','y'])
    actorChoices = []
    directorChoices= []
    years = []

    for i in range(3):
        if q == 'a':
            actorChoices.append(choice(actors))
        if q == 'd':
            directorChoices.append(choice(directors))
        if q == 'y':
            m = choice(movies)
            years.append(m['year'])
            years.append(int(m['year']) - choice(range(5,12)))
            break

    ind = choice(range(3))
    print('Are you ready?')
    print('...')
    sys.stdout.flush()
    if q == 'a':
        movie['actors'] = getActors(movie['link'])
        actorChoices.insert(ind, movie['actors'][0])
        print('Which one of the following starred in', movie['title'], '?')

        for a in actorChoices:
            print(actorChoices.index(a),a)
        
        answer = input()
        if int(answer) == actorChoices.index(movie['actors'][0]):
            print("CORRECT")
            player['score'] += 10
            sys.stdout.flush()
        else:
            print("WRONG")
            print(movie['actors'][0])
            sys.stdout.flush()
        
    if q == 'd':
        movie['director'] = getDirector(movie['link'])
        directorChoices.insert(ind, movie['director'])
        
        print('Who is the director of', movie['title'], '?')
        for d in directorChoices:
            print(directorChoices.index(d),d)

        answer = input()
        if int(answer) == directorChoices.index(movie['director']):
            print("CORRECT")
            player['score'] += 10
            sys.stdout.flush()
        else:
            print("WRONG")
            print(movie['director'])
            sys.stdout.flush()
        
    if q == 'y':
        years.append(int(movie['year']) - choice(range(8,12)))
        years.insert(ind, movie['year'])    
        print('When was the movie', movie['title'], ' premiered?')
        for y in years:
            print(years.index(y),y)
        answer = input()
        if int(answer) == years.index(movie['year']):
            print("CORRECT")
            player['score'] += 10
            sys.stdout.flush()
        else:
            print("WRONG")
            print(movie['year'])
            sys.stdout.flush()
   
init()
for i in range(10):
    randomQuestion()
    print()
print("Your score is: ", player['score'])
    
