# Python mingw library creator script
#### written in Python (ironically)

Creates MinGW compatible library files of the Python DLL using gendef/dlltool, for people too lazy to cross compile python.

### Supports:
 - Python 3.6.1
 - Win64 and 32 (64 tesred only)

### Requires: 
 - gendef (part of mingw)
 - dlltool (so is this)
 - Python 2

### How to run:

    make PREFIX={INSTALL_FOLDER} GENDEF={FULL_PATH_TO_GENDEF} DLLTOOL={FULL_PATH_TO_DLLTOOL}
	
`INSTALL_FOLDER` should probably be your MinGW prefix (where lib/include folders are)