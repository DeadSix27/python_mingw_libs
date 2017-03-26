# Python mingw library creator script
#### written in Python (ironically)

Creates MinGW compatible library files using gendef/dlltool, for people too lazy to cross compile python.

### Requires: 
 - gendef (part of mingw)
 - dlltool (so is this)
 - Python 2

### How to run:

    make PREFIX={INSTALL_FOLDER} GENDEF={FULL_PATH_TO_GENDEF} DLLTOOL={FULL_PATH_TO_DLLTOOL}
	
`INSTALL_FOLDER` should probably be your MinGW prefix (where lib/include folders are)