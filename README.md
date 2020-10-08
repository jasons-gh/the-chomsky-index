# The Chomsky Index

A minimalist program indexing the content of Noam Chomsky.

## Download

### Windows

Download The_Chomsky_Index.exe from [releases](https://github.com/jasons-gh/the-chomsky-index/releases).

## Install from source with pyinstaller

Before using pyinstaller run

    pip install -r requirements.txt

### Windows

    pyinstaller --icon=icon_black.ico --add-data cnt/*.cnt;cnt --add-data icon_white.png;png -w --onefile display.py

### Mac/Linux

    pyinstaller --icon=icon_black.icns --add-data cnt/*.cnt:cnt --add-data icon_white.png:png -w --onefile display.py

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