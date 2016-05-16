import requests, os, json
from bs4 import BeautifulSoup as BS
from random import choice

_BASE_PATH       = os.path.dirname(__file__)

_DATA_FILE       = os.path.join(_BASE_PATH,'data.txt')
_ACTORS_FILE     = os.path.join(_BASE_PATH,'actors.txt')
_DIRECTORS_FILE  = os.path.join(_BASE_PATH,'directors.txt')
_YEARS_FILE      = os.path.join(_BASE_PATH,'years.txt')

_IMDB_LIST       = r"http://www.imdb.com/chart/top?ref_=nv_mv_250_6"
_IMDB_BASE_URL   = r"http://www.imdb.com"

_movies          = []
_actorsPool      = []
_directorsPool   = []
_yearsPool       = []

def _getActorPool():
    actors = set()
    
    for m in _movies:
        for a in _getActorsForMovie(m['link']):
            actors.add(a)
        if len(actors) >= 100:
            break
        
    return list(actors)

def _getDirectorPool():
    directors = set()
    
    for m in _movies:
        directors.add(_getDirectorForMovie(m['link']))
        if len(directors) >= 100:
            break
        
    return list(directors)

def _getYearPool():
    years = set()
    
    for m in _movies:
        years.add(m['year'])
        
    return list(years)

def _init():
    global _movies
    global _actorsPool
    global _directorsPool
    global _yearsPool

    try:
        file    = open(_DATA_FILE)
        _movies  = eval(file.read())
        file.close()
    except FileNotFoundError:
        file    = open(_DATA_FILE, 'w')
        _movies  = _getMovies()
        file.write(str(_movies))
        file.close()

    try:
        file        = open(_ACTORS_FILE)
        _actorsPool  = list(eval(file.read()))
    except FileNotFoundError:
        file        = open(_ACTORS_FILE, 'w')
        _actorsPool  = _getActorPool()
        file.write(str(_actorsPool))
        file.close()

    try:
        file            = open(_DIRECTORS_FILE)
        _directorsPool   = list(eval(file.read()))
    except FileNotFoundError:
        file            = open(_DIRECTORS_FILE, 'w')
        _directorsPool   = _getDirectorPool()
        file.write(str(_directorsPool))
        file.close()
    
    try:
        file        = open(_YEARS_FILE)
        _yearsPool   = list(eval(file.read()))
    except FileNotFoundError:
        file        = open(_YEARS_FILE, 'w')
        _yearsPool   = _getYearPool()
        file.write(str(_yearsPool))
        file.close()

def _getMovies():
    response    = requests.get(_IMDB_LIST, headers = {'accept-language': 'en-US, en'})
    text        = response.text
    soup        = BS(text, 'html.parser')
    movieList   = []
    
    for line in soup.findAll('td', {"class": "titleColumn"}):
        m = dict()
        m['link']                   = _IMDB_BASE_URL + line.find('a').attrs['href']
        m['title']                  = line.find('a').text
        m['year']                   = (line.find('span').text)[1:-1]
        m['actors'],m['director']   = _getActorsAndDirector(m['link'])
        
        movieList.append(m)

    return movieList

def _getActorsForMovie(link):
    text    = requests.get(link).text
    soup    = BS(text, 'html.parser')
    actors  = []

    for line in soup.findAll('span', {"itemprop": "actors"}):
        name = line.find('span',{"itemprop":"name"}).text
        actors.append(name)
        
    return actors

def _getDirectorForMovie(link):
    text    = requests.get(link).text
    soup    = BS(text, 'html.parser')

    return (soup.find('span', {"itemprop": "director"})).find('span', {"itemprop":"name"}).text

def _getActorsAndDirector(link):
    text    = requests.get(link).text
    soup    = BS(text, 'html.parser')
    actors  = []

    for line in soup.findAll('span', {"itemprop": "actors"}):
        name = line.find('span',{"itemprop":"name"}).text
        actors.append(name)
        
    director = (soup.find('span', {"itemprop": "director"})).find('span', {"itemprop":"name"}).text
    return actors,director

def getRandomQuestion(nrOfChoices=4):
    if not (_movies and _actorsPool and _directorsPool and _yearsPool):
        _init()  # Making sure everything is set up, none of these
                # variables should be empty
    
    # Get random movie
    movie        = choice(_movies)
    group        = {'a': ['actors', _actorsPool, 'Who of the following starred in {0}?'],
                    'd': ['director', _directorsPool, 'Who was the director of {0}?'],
                    'y': ['year', _yearsPool, 'When was the movie {0} premeried?']}
    
    choices      = []
    questionType = choice(['a','d','y'])   # a for actor, d for director, y for year
                                           
    if questionType == 'a':
        correctAnswer = choice(movie[group[questionType][0]])
    else:
        correctAnswer = movie[group[questionType][0]]

    pool    = set(group[questionType][1])
    exclude = set(movie[group[questionType][0]])
    pool    = list(pool-exclude)

    for i in range(nrOfChoices-1):
        filler = choice(pool)
        pool.remove(filler)
        choices.append(filler)
        
    choices.insert(choice(range(3)), correctAnswer)
    jsonObj = json.dumps({'question':group[questionType][2].format(movie['title']),
            'choices': choices,
            'answer': correctAnswer})
    return jsonObj

'''
    TO BE ABLE TO USE THE MODULE AS A SCRIPT AS WELL
'''
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Y U so stupid!?')
    parser.add_argument('-q', '--questions', help='number of questions to return', type=int, nargs=1, default=1)
    parser.add_argument('-d', '--difficulty', help='difficulty,defined by number of choices', type=int, choices=range(2, 11),default=4)
    parser.add_argument('-k', '--keep-them-coming', help='continue getting questions until input is other than y/Y', action='store_true')

    args = parser.parse_args()
    
    for i in range(args.questions):
        print(getRandomQuestion(args.difficulty))

    if args.keep_them_coming:
        userInput = ""
        while True:
            answer = input('\nKeep them coming? (y):')
            if not(str(answer).lower() == 'y' or answer.lower() == 'yes'):
                exit()
            print(getRandomQuestion(args.difficulty))
        
