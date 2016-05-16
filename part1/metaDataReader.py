import stagger
import os
import sys
from stagger.id3 import *


def metaHound(argvPath):
    #ef það er sendur parametri inní fallið þá er það slóðin a möppuna
    #sem á að fara i gegnum.
    #ef ekki er sendur parameter er reiknað með að mappan sem á að fara
    #í gegnum sé í cwd.
    if argvPath != '':
        os.chdir(argvPath)
        os.chdir('..')
        ipodFolder = argvPath
    else:
        ipodFolder = os.path.join(os.getcwd(), 'ipod')
    if not os.path.exists(os.path.join(os.getcwd(), 'Music')):
        os.mkdir('Music')
    root = os.path.join(os.getcwd(), 'Music')
    #Búið að búa til Music möppu ef hún er ekki til og stilla current working directory á hana

    for data in os.walk(ipodFolder):
        for file in data[2]:
            #data[2] því við viljum bara skoða fæla, ekki folera
            os.chdir(root)
            #passa að í byrjun hvers hrings sé cwd alltaf Music mappan
            currPath = os.path.join(data[0], file)
            filename, extension = os.path.splitext(file)
            try:
                tag = stagger.read_tag(currPath)
                #ná í meta-data
                album = tag.album
                artist = tag.artist
                title = tag.title
                
                if artist == '':
                    artist = 'unknown artists'
                if album == '':
                    album = 'unknown albums'

                artist = fixName(artist)
                album = fixName(album)
                title = fixName(title)
                #taka burtu óleyfileg tákn

                artistPath = os.path.join(root, artist)
                if not os.path.exists(artistPath):
                    os.mkdir(artist)
                os.chdir(artistPath)
                #búa til möppu ef þarf fyrir þennan artista
                #stilla current working directory á þá möppu
                    
                albumPath = os.path.join(artistPath, album)
                if not os.path.exists(albumPath):
                    os.mkdir(album)
                os.chdir(albumPath)
                #búa til möppu inní artistanum fyrir plötuna
                #stilla current working directory á þá möppu
                
                newPath = os.path.join(albumPath, title + extension)
                if not os.path.exists(newPath):
                    os.rename(currPath, newPath)
                else:
                    os.remove(currPath)
                #færa lagið í album möppuna ef það er ekki þar nú þegar, annars er því eytt
            
            except:
                #hingað ef tekst ekki að ná i meta-data
                
                path = os.path.join(root, 'unknown files')
                os.chdir(root)
                if not os.path.exists(path):
                    os.mkdir('unknown files')
                newPath = os.path.join(path, file)
                #Búa til unknown files möppu ef hún er ekki til
                
                if not os.path.exists(newPath):
                    os.rename(currPath, newPath)
                else:
                    os.remove(currPath)
                #færa lagið í unknown files möppuna ef það er ekki þar nú þegar, annars er því eytt

    #henda ipod möppunni ef allt er tómt
    for folder in os.listdir(ipodFolder):
        os.removedirs(os.path.join(ipodFolder, folder))
    
def fixName(name):
    #ef nafnið inniheldur ólöglega caractera er þeim skipt út fyrir kommu
    return name.replace('\\', ',').replace('/', ',').replace(':', ',').replace('*', ',').replace('?', ',').replace('"', ',').replace('<', ',').replace('>', ',').replace('|', ',')

try:
    metaHound(sys.argv[1])
except:
    metaHound('')

























