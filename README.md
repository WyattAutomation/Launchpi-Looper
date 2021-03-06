# Launchpi-Looper
Simple Audio Sample Looping with a Raspberry Pi, and a Novation Launchpad MIDI Controller

This is a quick upload of edited example code from https://github.com/eavelardev/novation-launchpad which is based on FMMT666's Launchpad.py that you can find here: https://github.com/FMMT666/launchpad.py

The point of this is to provide code and documentation on setup and usage of Novation Launchpad MIDI controllers with a Raspberry Pi or similar cheap ARM board for looping audio samples in a live music context.  I will update this soon to include mmore detailed installation and useage instructions, and possibly an image of Raspbian Buster with everything presintalled.

## Getting Started

Install all of the prerequisites for this repository, and clone it:
https://github.com/eavelardev/novation-launchpad

Install pygame (if you're using Raspbian Buster, it should already be installed):
https://www.pygame.org/wiki/GettingStarted

Download and copy clip_looper.py from this repo to the cloned novation_launchpad/examples directory from above

Edit clip_looper.py for compatiblity with your model of Launchpad

Create a directory named "samples" in the novation_launchpad/examples directory

Change the line that has:
```
rootdir = "/home/ubuntu/novation-launchpad/examples/samples/"
```
from "ubuntu" to your own username.

In this "samples" directory, you can create folders with names **ENDING** with numbers 1-8.  For example, you might name one folder "drumbeatloops-1".  Inside of these folders, you can add 16 bit wav files **STARTING** with numbers 1-8.  For example, you might name your audio file "3-drumbeat.wav" and so on.  The 1-8 number on the end of the folder names, corresponds to which **ROW** of pads you want the samples in that folder to be added to.  The 1-8 number on the beginning of the wav audio file's name corresponds to which **COLUMN** of pads you want that audio file to be on, per it's folder's specified row.    

All samples are loaded to pads per the above explanation, which should show up with a green-lit LED on the corresponding pad.  They all are initialized as "playing" but on mute, and pushing the associated pad unmutes it and turns the pad red.  Pushing it again turns it green again and mutes it.  

As it is now, make sure your samples are all in the same BPM, and are of the same length.  I will update this as soon as I can to auto-crop and timewarp samples to an editable BPM from the unused buttons on the launchpad, but as it is now just be sure to know which rows you've loaded samples in which BPM ahead of time (not too hard to do, perhaps name your folders with the BPM as a reminder).
