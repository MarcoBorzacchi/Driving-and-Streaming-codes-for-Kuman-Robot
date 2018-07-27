#!/bin/bash
# Ask the user for their name

echo Are you local or remote? -l or -r
read varname
if [ $varname == 'l' ] 
then
	python stream.py | sudo  python gui_py2.py
elif [ $varname = 'r' ]
then
	python stream.py | python remote_tcp.py
	
else

	. ./robot

fi


