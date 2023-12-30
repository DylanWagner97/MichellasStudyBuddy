from tkinter import ttk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import tkinter as Tk
from os.path import basename, expanduser, isfile, join as joined
from pathlib import Path
import time
import sys
import os
import vlc

_isLinux = False
_isWindows = True
videoList = []
videoIndex = 0
startedPlayer = False
stopped = True

for video in os.listdir("./Videos"):
    if video.endswith(".mp4"):
        videoList.append(video)
window = Tk.Tk() #Create 
window.geometry("%dx%d" % (window.winfo_screenwidth(), window.winfo_screenheight()))
window.title("Michella Study Buddy")

icon = PhotoImage(file='logo.png')
window.iconphoto(True, icon)

window.config(background="black")
if (videoList[0]):
    window.config(background="pink")


class Player(Tk.Frame):
    def __init__(self, parent, title=None, video=''):
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        self.video = "./Videos/" + videoList[0]
        self.videopanel = ttk.Frame(self.parent)
        self.canvas = Tk.Canvas(self.videopanel)
        self.canvas.pack(fill=Tk.BOTH, expand=1)
        self.videopanel.pack(fill='both', expand=1)
        self.buttons_panel = Tk.Toplevel(window)

        self.buttons_panel.title("")
        buttons = ttk.Frame(self.buttons_panel)
        self.previousButton = ttk.Button(buttons, text="Prev", command= self.previousVideo)
        self.playButton = ttk.Button(buttons, text="Play", command= self.playVideo)
        self.nextButton = ttk.Button(buttons, text="Next", command = self.nextVideo)
        self.previousButton.pack(side= LEFT)
        self.playButton.pack(side= LEFT)
        self.nextButton.pack(side= LEFT)
        self.mute = False
        self.volume = Tk.IntVar()
        self.volume.set(100)
        self.volSlider = Tk.Scale(buttons, variable=self.volume, command= self.OnVolume, from_=0, to=100, orient=Tk.HORIZONTAL, length=window.winfo_screenwidth()/10, showvalue=100, label='Volume')
        self.volSlider.pack(side= RIGHT)
        buttons.pack(side= BOTTOM)
        timers = ttk.Frame(self.buttons_panel)
        self.timeVar = Tk.DoubleVar()
        self.timeSliderLast = 0
        self.timeSlider = Tk.Scale(timers, variable=self.timeVar, command= self.OnTime,
                                   from_=0, to=100, orient=Tk.HORIZONTAL, length=window.winfo_screenwidth()/4,
                                   showvalue=0)  # label='Time',
        self.timeSlider.pack(side=Tk.BOTTOM, fill=Tk.X, expand=1)
        self.timeSliderUpdate = time.time()
        timers.pack(side=Tk.BOTTOM, fill=Tk.X)
        self.OnTick()
        # VLC player
        args = []
        if _isLinux:
            args.append('--no-xlib')
        Instance = vlc.Instance(args)
        self.player = Instance.media_player_new()
        self.parent.update()
        media = Instance.media_new("./Videos/" + videoList[videoIndex])
        self.player.set_media(media)
        if _isWindows:
            self.player.set_hwnd(self.videopanel.winfo_id())
        else:
            self.player.set_xwindow(self.videopanel.winfo_id())
        # After parent.update() otherwise panel is ignored.
        self.buttons_panel.attributes('-topmost', 'true')
        self.buttons_panel.geometry('+%d+%d' % (window.winfo_screenwidth()/2.25, window.winfo_screenheight()/1.2))
        self.buttons_panel.overrideredirect(True)

    def playVideo(play):
        global stopped
        if stopped:
            player.player.play()
            stopped = False
            player.OnTick()
        else: 
            player.player.pause()
            stopped = True
    
    def setupPlayer(play):
        args = []
        if _isLinux:
            args.append('--no-xlib')
        Instance = vlc.Instance(args)
        player.player = Instance.media_player_new()
        player.parent.update()
        media = Instance.media_new("./Videos/" + videoList[videoIndex])
        player.player.set_media(media)
        if _isWindows:
            player.player.set_hwnd(player.videopanel.winfo_id())
        else:
            player.player.set_xwindow(player.videopanel.winfo_id())

    def OnTick(play):
        if stopped == False and player:
            player.buttons_panel.lift()
            # since the self.player.get_length may change while
            # playing, re-set the timeSlider to the correct range
            t = player.player.get_length() * 1e-3  # to seconds
            if t > 0:
                player.timeSlider.config(to=t)

                t = player.player.get_time() * 1e-3  # to seconds
                # don't change slider while user is messing with it
                if t > 0 and time.time() > (player.timeSliderUpdate + 2):
                    player.timeSlider.set(t)
                    player.timeSliderLast = int(player.timeVar.get())
        # start the 1 second timer again
        if (stopped == False):
            window.after(1000, player.OnTick)

    def previousVideo(play):
        global videoIndex
        global stopped
        if player:
            player.player.stop()
            stopped = True
            player.timeSlider.set(0)
            if videoIndex == 0:
                videoIndex = len(videoList)-1
            else:
                videoIndex = videoIndex - 1
            player.setupPlayer()
            player.playVideo()
            
    def nextVideo(play):
        global videoIndex
        global stopped
        if player:
            player.player.stop()
            stopped = True
            player.timeSlider.set(0)
            if videoIndex == len(videoList) - 1:
                videoIndex = 0
            else:
                videoIndex = videoIndex + 1
            player.setupPlayer()
            player.playVideo()

    def OnVolume(play, volume):
        volume = player.volume.get()
        if volume > 100:
            volume = 100
        if player.player.audio_set_volume(volume) == -1:
            player.player.audio_set_volume(50)
        return True
    def OnTime(play, unused):
        if player:
            t = player.timeVar.get()
            if player.timeSliderLast != int(t):
                player.player.set_time(int(t * 1e3))
                player.timeSliderUpdate = time.time()

    def TouchVideo(play, test):
        player.playVideo()

        




    
    
    

player = Player(window)
label = Label(window, text="Merry Christmas Michella :)", font=('Arial', 25, 'bold'), bg='pink')
label.place(x= window.winfo_screenwidth()/2.4, y = window.winfo_screenheight()/2)
label.after(6000, label.destroy)
window.bind("<Button-1>", player.TouchVideo)
window.mainloop() #place window and listen for events

