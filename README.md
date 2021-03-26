# The Chomsky Index

A minimalist program indexing the content of Noam Chomsky.

## Download

### Windows

On Windows, download The_Chomsky_Index.exe [using this link](https://github.com/jasons-gh/the-chomsky-index/releases/download/v1.1.0/The_Chomsky_Index.exe). If SmartScreen appears, click *More info* then click *Run anyway*.

### macOS

On macOS, download The_Chomsky_Index.zip [using this link](https://github.com/jasons-gh/the-chomsky-index/releases/download/v1.1.0/The_Chomsky_Index.zip) and unzip it if needed. *The Chomsky Index.app* must then be moved once into a different location than the one into which it was extracted. Open it and exit the dialog that appears. Then *right-click* > *Open* > *Open*.

### Ubuntu

On Ubuntu, download The_Chomsky_Index.zip [using this link](https://github.com/jasons-gh/the-chomsky-index/releases/download/v1.1.0/The_Chomsky_Index.zip) and extract it. In the executable properties tick *Allow executing file as program*.

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

## Or install from source

Use Python 3.7 without Anaconda. Upgrade setuptools and install the requirements with

    pip3 install --upgrade setuptools
    pip3 install -r requirements.txt

Run the below commands based on your operating system.

### Windows

    pyinstaller --icon=icon_black.ico --add-data h5;h5 --add-data html;html --add-data icon_white.png;png -w -F display.py

### macOS

Rename *display.py* to *The Chomsky Index.py*. Then run
	
	python3 setup.py py2app

### Ubuntu

Make pyinstaller and PyQt5 available with

    export PATH=$PATH:/home/yourname/.local/bin
	
Fix a problem with the PyQt5 display with

    sudo apt-get install libxcb-xinerama0
	
Create the program in a folder called *dist* with

    pyinstaller --add-data h5:h5 --add-data html:html --add-data icon_white.png:png -w -F display.py

In the executable properties, change the icon to icon_black.ico from the repo.
