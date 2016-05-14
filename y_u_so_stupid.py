from pprint import pprint
import requests
import os
import sys
from bs4 import BeautifulSoup as BS
from random import choice
import sys
import json

BASE_PATH       = os.path.dirname(__file__)

DATA_FILE       = os.path.join(BASE_PATH,'data.txt')
ACTORS_FILE     = os.path.join(BASE_PATH,'actors.txt')
DIRECTORS_FILE  = os.path.join(BASE_PATH,'directors.txt')
YEARS_FILE      = os.path.join(BASE_PATH,'years.txt')

IMDB_LIST       = r"http://www.imdb.com/chart/top?ref_=nv_mv_250_6"
IMDB_BASE_URL   = r"http://www.imdb.com"

movies          = []
actorsPool      = []
directorsPool   = []
yearsPool       = []

def getActorPool():
    actors = set()
    
    for m in movies:
        for a in getActorsForMovie(m['link']):
            actors.add(a)
        if len(actors) >= 100:
            break
        
    return list(actors)

def getDirectorPool():
    directors = set()
    
    for m in movies:
        directors.add(getDirectorForMovie(m['link']))
        if len(directors) >= 100:
            break
        
    return list(directors)

def getYearPool():
    years = set()
    
    for m in movies:
        years.add(m['year'])
        
    return list(years)

def init():
    global movies
    global actorsPool
    global directorsPool
    global yearsPool

    try:
        file    = open(DATA_FILE)
        movies  = eval(file.read())
        file.close()
    except FileNotFoundError:
        file    = open(DATA_FILE, 'w')
        movies  = getMovies()
        file.write(str(movies))
        file.close()

    try:
        file        = open(ACTORS_FILE)
        actorsPool  = list(eval(file.read()))
    except FileNotFoundError:
        file        = open(ACTORS_FILE, 'w')
        actorsPool  = getActorPool()
        file.write(str(actorsPool))
        file.close()

    try:
        file            = open(DIRECTORS_FILE)
        directorsPool   = list(eval(file.read()))
    except FileNotFoundError:
        file            = open(DIRECTORS_FILE, 'w')
        directorsPool   = getDirectorPool()
        file.write(str(directorsPool))
        file.close()
    
    try:
        file        = open(YEARS_FILE)
        yearsPool   = list(eval(file.read()))
    except FileNotFoundError:
        file        = open(YEARS_FILE, 'w')
        yearsPool   = getYearPool()
        file.write(str(yearsPool))
        file.close()

def getMovies():
    response    = requests.get(IMDB_LIST, headers = {'accept-language': 'en-US, en'})
    text        = response.text
    soup        = BS(text, 'html.parser')
    movieList   = []
    
    for line in soup.findAll('td', {"class": "titleColumn"}):
        m = dict()
        m['link']                   = IMDB_BASE_URL + line.find('a').attrs['href']
        m['title']                  = line.find('a').text
        m['year']                   = (line.find('span').text)[1:-1]
        m['actors'],m['director']   = getActorsAndDirector(m['link'])
        
        movieList.append(m)

    return movieList

def getActorsForMovie(link):
    text    = requests.get(link).text
    soup    = BS(text, 'html.parser')
    actors  = []

    for line in soup.findAll('span', {"itemprop": "actors"}):
        name = line.find('span',{"itemprop":"name"}).text
        actors.append(name)
        
    return actors

def getDirectorForMovie(link):
    text    = requests.get(link).text
    soup    = BS(text, 'html.parser')

    return (soup.find('span', {"itemprop": "director"})).find('span', {"itemprop":"name"}).text

def getActorsAndDirector(link):
    text    = requests.get(link).text
    soup    = BS(text, 'html.parser')
    actors  = []

    for line in soup.findAll('span', {"itemprop": "actors"}):
        name = line.find('span',{"itemprop":"name"}).text
        actors.append(name)
        
    director = (soup.find('span', {"itemprop": "director"})).find('span', {"itemprop":"name"}).text
    return actors,director

def getRandomQuestion():
    if not (movies and actorsPool and directorsPool and yearsPool):
        init()  # Making sure everything is set up, none of these
                # variables should be empty
    
    # Get random movie
    movie        = choice(movies)
    group        = {'a': ['actors',actorsPool, 'Who of the following starred in {0}?'],
                    'd': ['director',directorsPool, 'Who was the director of {0}?'],
                    'y': ['year',yearsPool, 'When was the movie {0} premeried?']}
    
    choices      = []
    questionType = choice(['a','d','y'])   # a for actor, d for director, y for year
                                           
    if questionType == 'a':
        correctAnswer = choice(movie[group[questionType][0]])
    else:
        correctAnswer = movie[group[questionType][0]]
        
    for i in range(3):
        pool = list(set(group[questionType][1]) - set(movie[group[questionType][0]]))
        choices.append(choice(pool))
        
    choices.insert(choice(range(3)), correctAnswer)
    return json.dumps({'question':group[questionType][2].format(movie['title']),
            'choices': choices,
            'answer': correctAnswer})

