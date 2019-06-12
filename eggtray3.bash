#!/bin/bash

echo "Please enter the tray ID"
read trayID
#Creates the directory, if it exists, throws an error. 
mkdir "$trayID"
traydir=`pwd`"/$trayID"
for i in {a1,a2,b1,b2,c1,c2,d1,d2,e1,e2,f1,f2,g1,g2}; do
	echo "Hit return to capture image $trayID$i.png"
	read INPUT
	#Take an image
	raspistill -e png -roi .2,.2,.675154321,.7716049383 -w 1750 -h 1500 -awb fluorescent -ss 2500 -o "$trayID$i".png
	#Force move the image, will not create a directory, will overwrite image of the same name
	mv -f "$trayID$i".png "$trayID"/"$trayID$i".png
done
python $SCRIPTS_DIR"eggthresh3.py" run_directory $traydir
