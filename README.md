# Python mingw library creator script
#### written in Python (ironically)

Creates mingw compatible library files using gendef/dlltool, for people too lazy to cross compile python.

Requires: 
* gendef
* dlltool
* Python 2+

How to run:
	`make PREFIX={INSTALL_FOLDER} GENDEF={FULL_PATH_TO_GENDEF} DLLTOOL=FULL_PATH_TO_DLLTOOL`
	
`INSTALL_FOLDER` should probably be your mingw root (where lib/include folders are)