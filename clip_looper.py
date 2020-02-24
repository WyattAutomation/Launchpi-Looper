import os
import wave
import sys
import pygame
import numpy as np
import pyaudio
import novation_launchpad as launchpad
import rtmidi
import time

# -----------------------------
# |   [0,0] ... [7,0]         |
# | -------------------       |
# | | [0,1] ... [7,1] | [8,1] |
# | |  ...       ...  |  ...  |
# | | [0,8] ... [7,8] | [8,8] |
# | -------------------       |
# -----------------------------

grid_octave = 2


layout_mask1 = [[28,29,30,31,32,33,34,35],
                [24,25,26,27,36,37,38,39],
                [20,21,22,23,40,41,42,43],
                [16,17,18,19,44,45,46,47],
                [12,13,14,15,48,49,50,51],
                [ 8, 9,10,11,52,53,54,55],
                [ 4, 5, 6, 7,56,57,58,59],
                [ 0, 1, 2, 3,60,61,62,63]]

layout_mask2 = [[28,29,30,31,60,61,62,63],
                [24,25,26,27,56,57,58,59],
                [20,21,22,23,52,53,54,55],
                [16,17,18,19,48,49,50,51],
                [12,13,14,15,44,45,46,47],
                [ 8, 9,10,11,40,41,42,43],
                [ 4, 5, 6, 7,36,37,38,39],
                [ 0, 1, 2, 3,32,33,34,35]]

layout_mask3 = [[28,29,30,31,32,33,34,35],
                [27,26,25,24,39,38,37,36],
                [20,21,22,23,40,41,42,43],
                [19,18,17,16,47,46,45,44],
                [12,13,14,15,48,49,50,51],
                [11,10, 9, 8,55,54,53,52],
                [ 4, 5, 6, 7,56,57,58,59],
                [ 3, 2, 1, 0,63,62,61,60]]

layout_mask4 = [[56,57,58,59,60,61,62,63],
                [48,49,50,51,52,53,54,55],
                [40,41,42,43,44,45,46,47],
                [32,33,34,35,36,37,38,39],
                [24,25,26,27,28,29,30,31],
                [16,17,18,19,20,21,22,23],
                [ 8, 9,10,11,12,13,14,15],
                [ 0, 1, 2, 3, 4, 5, 6, 7]]

layout_mask5 = [[63,62,61,60,59,58,57,56],
                [48,49,50,51,52,53,54,55],
                [47,46,45,44,43,42,41,40],
                [32,33,34,35,36,37,38,39],
                [31,30,29,28,27,26,25,24],
                [16,17,18,19,20,21,22,23],
                [15,14,13,12,11,10, 9, 8],
                [ 0, 1, 2, 3, 4, 5, 6, 7]]

colors =   [[30, 0, 0],     # 0. middle_c/error
            [0, 10, 30],    # 1. root
            [10, 10, 15],   # 2. white_key/ok
            [0, 0, 0],      # 3. black_key
            [0, 50, 0]]     # 4. pressed

class MidiInputHandler(object):
    def __init__(self, lp):
        self.lp = lp
        self.init_note = grid_octave * 12
        self.velocity = 100
        self.pads_type = None
        self.notes_out = None
        self.my_layout = layout_mask5
        self.midiout = rtmidi.MidiOut()
        self.midiout.open_virtual_port("Grid Instrument")
        self.ledtracker = []
        pygame.init()
        pygame.mixer.set_num_channels(64)
        self.samples = []
        self.tunes = []
        self.update_layout()

    def __call__(self, event, data=None):
        #self.player = WavePlayerLoop("beat1.wav")
        msg, _ = event
        self.lp.msg = msg

        but = self.lp.ButtonStateXY()
        self.lp.msg = None
        npsamps = np.array(self.samples)
        #nptunes = np.array(self.tunes)
        x = but[0]
        y = but[1]
        #pressed = but[2] is 127
        self.checkxy = [x, y]
        if x < 8 and y > 0:
            if but[2]>0:
                self.midiout.send_message([144, self.notes_out[y-1][x], self.velocity])
                self.lp.LedCtrlXY(x, y, 30, 0)
                result = np.where((npsamps[:,0] == x) * (npsamps[:,1] == y))
                tmpIdx = int(result[0])
                if self.checkxy in self.ledtracker:
                    print("if")
                    print(tmpIdx)
                    self.tunes[tmpIdx][1].set_volume(0)
                    self.lp.LedCtrlXY(x, y, 0, 30)
                    self.ledtracker.remove(self.checkxy)
                else:
                    print("else")
                    print(tmpIdx)
                    self.tunes[tmpIdx][1].set_volume(1)
                    self.ledtracker.append(self.checkxy)
                    self.lp.LedCtrlXY(x, y, 30, 0)
            # else:
            #     self.midiout.send_message([128, self.notes_out[y-1][x], 0])
            #     self.lp.LedCtrlXY(x, y, 0, 30)
        # if x is 0 and y is 0:
        #     if but[2]>0:
        #         print("pushed")
        #         if self.init_note + 1 <= 48:    # increase one note
        #             self.init_note += 1
        #             self.lp.LedCtrlXY(x, y, 0, 30)
        #             self.update_layout()
        #         else:
        #             self.lp.LedCtrlXY(x, y, 0, 30)
        #     else:
        #             self.lp.LedCtrlXY(x, y, 0, 30)
        # if x is 1 and y is 0:
        #     if but[2]>0:
        #         print("pushed")
        #         if self.init_note - 1 >= 20:    # decrease one note
        #             self.init_note -= 1
        #             self.lp.LedCtrlXY(x, y, 0, 30)
        #             self.update_layout()
        #         else:
        #             self.lp.LedCtrlXY(x, y, 0, 30)
        #     else:
        #             self.lp.LedCtrlXY(x, y, 0, 30)

    def update_layout(self):
        self.notes_out = [[val + self.init_note for val in row] for row in self.my_layout]

        self.pads_type = []

        for row in self.notes_out:
            new_row = []
            for val in row:
                if val is 60:
                    new_row.append(0)
                elif val % 12 is 0:
                    new_row.append(1)
                elif val % 12 in [2,4,5,7,9,11]:
                    new_row.append(2)
                else:
                    new_row.append(3)
            self.pads_type.append(new_row)
        channels = 0
        rootdir = "/home/ubuntu/novation-launchpad/examples/samples/"
        for subdir, dirs, files in os.walk(rootdir):
            for filename in files:
                filepath = subdir + os.sep + filename
                print(filepath)
                print("y is: " + subdir[-1] + "  x is: " + filename[0])
                print("\n")
                y = int(subdir[-1])
                x = int(filename[0]) - 1
                self.lp.LedCtrlXY(x, y, 0, 30)
                beat = pygame.mixer.Sound(str(filepath))
                free_channel = pygame.mixer.find_channel()
                free_channel.set_volume(0)
                free_channel.play(beat, loops=-1)
                tune = [beat, free_channel]
                samp = [x, y]
                self.samples.append(samp)
                self.tunes.append(tune)


def main():
    lp = launchpad.Launchpad()

    if lp.Open( 0, "mini" ):
        print( " - Launchpad mini: OK" )
    else:
        print( " - Launchpad mini: ERROR" )
        return

    lp.midi.devIn.set_callback(MidiInputHandler(lp))

    print("Entering main loop. Press Control-C to exit.")
    try:
        while True:
            #print("duuuuuh")
            time.sleep(1)         
    except KeyboardInterrupt:
        print('')
    finally:
        print("Exit.")
        lp.Reset()
        lp.Close()

if __name__ == '__main__':
    main()
