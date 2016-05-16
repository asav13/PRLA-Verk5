# Y U so stupid - A Python Meta-Data Reader
Reykjavík University, May 2016<br>
T-308-PRLA - The Python Programming Language<br>
Assignment nr 5<br>
Authors: asav13@ru.is, vedise13@ru.is

A python script that scans music files for metadata and organizes them by artists and albums.

## Installation and dependencies

In order for everything to work properly you must have Python3 installed, and some pip packages:
-stagger

to install the packages simply run:
```
	python -m pip install stagger
```
Note however that depending on your OS, the command could be simple pip install <packagename> or py -m pip install <packagename>

###Run the script

##Without a parameter
Run
```py metaDataReader.py```
The script will assume that the folder it should go through is called *ipod* and is located in the same folder as *metaDataReader.py*. The result will be located in the same folder.

##With a parameter
Run
```py metaDataReader.py C:\\path\\to\\folder\\holding\\data```
The script will go through that folder and place the result in that folder's parent folder.


###Code
1. First we check if the program was provided with a path to a folder and set up current working directory according to that.

2. If there is no *Music* folder, it is created and result will then be stored there.

3. The folder is walked through using *os.walk()*. Every file in that folder will be checked for meta-data.
If no meta-data is found, the file will be moved to a folder called *unknown files*, located in the *Music* folder.
If meta-data is found, title, artist and album are saved as string variables and all illegal characters removed from them, folders created if needed and then the file replaced and renamed.

4. The original folder that held the data is deleted.
