# The Chomsky Index

A minimalist program indexing the content of Noam Chomsky.

## Download

### Windows

On Windows, download The_Chomsky_Index.exe [using this link](https://github.com/jasons-gh/the-chomsky-index/releases/download/v1.0.0/The_Chomsky_Index.exe), which should require no further setup.

## Install from source with pyinstaller

First install the requirements with

    pip3 install -r requirements.txt

### Windows

    pyinstaller --icon=icon_black.ico --add-data cnt/*.cnt;cnt --add-data icon_white.png;png -w --onefile display.py

### Mac

    pyinstaller --icon=icon_black.icns --add-data cnt/*.cnt:cnt --add-data icon_white.png:png -w --onefile display.py

### Linux

Do not use anaconda or miniconda. Make pyinstaller and PyQt5 available with

    export PATH=$PATH:/home/yourname/.local/bin
	
Fix a problem with the PyQt5 display with

    sudo apt-get install libxcb-xinerama0
	
Create the program in a folder called *dist* with

    pyinstaller --add-data cnt/*.cnt:cnt --add-data icon_white.png:png -w --onefile display.py

In the executable properties, change the icon to icon_black.ico from the repo.

## Usage

### Normal search

Use *math* to search for results containing *math*, for example in *math*, *maths*, *mathematics*, *metamathematics* and *aftermath*.

### Separate search

Use *anarchism; communism; fascism* to search for results with all of *anarchism*, *communism* and *fascism*. Useful in searching for multiple topics mentioned within the same result.

### Nearby search

Use *bertrand russell + rosa luxemburg* to search for results with *bertrand russell* and *rosa luxemburg* nearby. Useful in searching for quotes.

## Examples

### Using a normal search to find occurrences of *haiti*

![examples/tci_normal.gif](examples/tci_normal.gif)

<br/>

<br/>

<br/>

<br/>

### Using a separate search to find results that contain *arithmetic* and *atoms*

![examples/tci_separate.gif](examples/tci_separate.gif)

<br/>

<br/>

<br/>

<br/>

### Using a nearby search to find the source of a quote

![examples/tci_nearby.gif](examples/tci_nearby.gif)