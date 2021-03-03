#!/bin/bash
for N in {10..1}
do
	echo $N'sec'
	env sleep 1
done

TODAY=$(date +'%Y-%m-%d_%H:%M:%S')
echo $TODAY
/usr/bin/python3 /home/pi/Desktop/record-It/recorder.py
