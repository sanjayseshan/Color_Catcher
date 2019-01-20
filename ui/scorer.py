#!/usr/bin/python
# -*- coding: utf-8 -*-
# Echo server program
import time
import os
import socket
import threading
import struct
import evdev
from time import sleep
import random

device = evdev.InputDevice('/dev/input/event0')
print(device)

locations = {"none": (0,0), "black": (0,0), "blue" : (0,3),"green": (0,0),"yellow": (4,1),"red": (0,0),"white": (0,0), "brown": (0,0)}
set = [0]*6
scores = {"red":0, "green":0, "yellow":0, "Reset":-1, "main":-1}
loc = 'green:(0,0)'

enToDa = {"bkg-en.png":"bkg-da.png", "Game Over":"Spillet er slut", "Yellow Robot Wins":"Gul Robot Vinder", "Red Robot Wins":"Rød Robot Vinder","Orange Robot Wins":"Orange Robot Vinder"}
enToEs = {"bkg-en.png":"bkg-es.png", "Game Over":"Partido Completado", "Yellow Robot Wins":"Robot Armarillo Gana", "Red Robot Wins":"Robot Rojo Gana","Orange Robot Wins":"Robot Naranja Gana"}

possibleCols = ["red","blue","green","yellow","black","orange"]
drawcolors = {"red":'"rgb(255,0,0)"',"blue":'"rgb(0,0,255)"',"green":'"rgb(0,255,0)"',"yellow":"yellow","black":'"rgb(0,0,0)"',"orange":'"rgb(255,103,0)"'}

bkgPic = "bkg-en.png"
gameOver = "Game Over"
yelWon = "Yellow Robot Wins"
redWon = "Red Robot Wins"
greenWon = "Orange Robot Wins"

target = possibleCols[0]

botmax = 5 # winnning score for individual ghost

connections = []

yelold = 0
redold = 0
greenold = 0

reset = 0
need_reset = 0

touchx = 0
touchy = 0


def newTarget(lastTarget):
        targetL = possibleCols[random.randint(0,len(possibleCols)-1)]
        while targetL == lastTarget:
                targetL = possibleCols[random.randint(0,len(possibleCols)-1)]
                print("Target possibility: "+targetL)
        broadcast(targetL)
        return targetL
                
                
def broadcast(data):
        for (s, id) in connections:
           send_str = str(str(data)).encode()
           send_msg = struct.pack('!I', len(send_str))
           send_msg += send_str
           print("sending " + str(len(send_str)) + " bytes")
           print("sending total " + str(len(send_msg)) + " bytes")
           print("sending " + str(send_msg))
           try:
                   s.sendall(send_msg)
                   print("SENDING COMPLETE")
                   #      data = s.recv(1024)
           except Exception as e:
                   print("FAILURE TO SEND.." + str(e.args) + "..RECONNECTING")
                   try:
                           print("sending " + send_msg)
                           s.sendall(send_msg)
                           #         data = s.recv(1024)
                   except:
                           print("FAILED.....Giving up :-( - pass;")
                           pass

def updatedata(caller):
        global yelold,redold,greenold,need_reset,target,bkgPic,gameOver,yelWon,redWon,greenWon

        if caller != "Language" and caller != "Reset1" and caller != "Touch" and caller != "spinner":
                if scores[caller] != 0:
                        target = newTarget(target)
                        broadcast(target)
        print(bkgPic)
        print "Called by " + caller
#	print "Locations: " + str(locations)
	print "Yellow: " + str(scores["yellow"])
	print "Red: " + str(scores["red"])
	print "Green: " + str(scores["green"])
        print "Target: " + target
        print "Connected:"
#        print connections
        for (s, id) in connections:
                print id
        print "\n"

#        if need_reset:
#                return
        red = str(scores["red"])
        yel = str(scores["yellow"])
        green = str(scores["green"])
        
        if int(yel) > int(yelold):
	        os.system('echo seshan | sudo -S aplay point.wav &')
        if int(red) > int(redold):
	        os.system('echo seshan | sudo -S aplay point.wav &')
        if int(green) > int(greenold):
	        os.system('echo seshan | sudo -S aplay point.wav &')

#        os.system('convert -background black -fill white -size 16x16 -font Helvetica -pointsize 15 -gravity center label:"'+red+'" -threshold 50 -morphology Thinning:-1 "LineEnds:-1;Peaks:1.5" -depth 1 cmd1.png')
#        os.system('convert -background white -fill black -size 16x16 -font Helvetica -pointsize 15 -gravity center label:"'+green+'" -threshold 50 -morphology Thinning:-1 "LineEnds:-1;Peaks:1.5" -depth 1 cmd2.png')
        os.system('convert -background white -fill black -size 16x16 -font Helvetica -pointsize 15 -gravity center label:"'+red+'" -posterize 2 cmd1.png')
        os.system('convert -background white -fill black -size 16x16 -font Helvetica -pointsize 15 -gravity center label:"'+green+'" -posterize 2 cmd2.png')
        os.system('convert -background white -fill black -size 16x16 -font Helvetica -pointsize 15 -gravity center label:"'+yel+'" -posterize 2 cmd3.png')
#        os.system('convert -background white -fill black -size 16x16 -font Helvetica -pointsize 15 -gravity center label:"'+yel+'" -threshold 50 -morphology Thinning:-1 "LineEnds:-1;Peaks:1.5" -depth 1 cmd3.png')

#        os.system('convert -size 160x96 xc:black -fill red -draw "image over  0,0 0,0 \''+bkgPic+'\'"  -draw "image over  100,18 0,0 \'cmd1.png\'" -draw "image over  100,34 0,0 \'cmd2.png\'" -draw "image over  100,50 0,0 \'cmd3.png\'" -fill '+drawcolors[target]+' -stroke black -draw "rectangle 0,31 63,95" -fill black -draw "color '+str(touchx/5)+','+str(touchy/5)+' point"  cmd.png ')
        if caller == "Reset1":
                #os.system('cp cmd.png cmdtmp.png ; convert cmdtmp.png -fill none -stroke blue -strokewidth 3 -draw "rectangle 77,70 124,90" cmd.png')
                os.system('convert -size 160x96 xc:black -fill red -draw "image over  0,0 0,0 \''+bkgPic+'\'"  -draw "image over  100,18 0,0 \'cmd1.png\'" -draw "image over  100,34 0,0 \'cmd2.png\'" -draw "image over  100,50 0,0 \'cmd3.png\'" -fill '+drawcolors[target]+' -stroke black -draw "rectangle 0,31 63,95" -fill none -stroke blue -strokewidth 3 -draw "rectangle 77,70 124,90" -fill black -draw "image over '+str(touchx/5)+','+str(touchy/5)+' 0,0 mouse2.png"  cmd.png ')
        elif caller == "Language":
                os.system('convert -size 160x96 xc:black -fill red -draw "image over  0,0 0,0 \''+bkgPic+'\'"  -draw "image over  100,18 0,0 \'cmd1.png\'" -draw "image over  100,34 0,0 \'cmd2.png\'" -draw "image over  100,50 0,0 \'cmd3.png\'" -fill '+drawcolors[target]+' -stroke black -draw "rectangle 0,31 63,95" -fill black -draw "image over '+str(touchx/5)+','+str(touchy/5)+' 0,0 mouse2.png"  cmd.png ')
        else:
                os.system('convert -size 160x96 xc:black -fill red -draw "image over  0,0 0,0 \''+bkgPic+'\'"  -draw "image over  100,18 0,0 \'cmd1.png\'" -draw "image over  100,34 0,0 \'cmd2.png\'" -draw "image over  100,50 0,0 \'cmd3.png\'" -fill '+drawcolors[target]+' -stroke black -draw "rectangle 0,31 63,95" -fill black -draw "image over '+str(touchx/5)+','+str(touchy/5)+' 0,0 mouse1.png"  cmd.png ')

        if int(red) >= botmax or int(green) >= botmax or int(yel) >= botmax:
	        print "GAME OVER"
                need_reset = 1
                if caller != "Language" and caller != "Reset1" and caller != "Touch" and caller != "spinner":
	                os.system('echo seshan | sudo -S aplay win.wav &')
	        os.system('cp cmd.png cmdtmp.png')
	        if int(red) >= botmax :
		        os.system('convert cmdtmp.png -draw "rectangle 0,0 160,70" -font Helvetica -weight 700  -pointsize 15 -undercolor black -draw "gravity center fill white text 0,0 \''+gameOver+'\n'+redWon+'\' " cmd.png')
	        if int(green) >= botmax :
		        os.system('convert cmdtmp.png -draw "rectangle 0,0 160,70" -font Helvetica -weight 700  -pointsize 15 -undercolor black -draw "gravity center fill white text 0,0 \''+gameOver+'\n'+greenWon+'\' " cmd.png')
	        if int(yel) >= botmax :
		        os.system('convert cmdtmp.png -draw "rectangle 0,0 160,70" -font Helvetica -weight 700  -pointsize 15 -undercolor black -draw "gravity center fill white text 0,0 \''+gameOver+'\n'+yelWon+'\' " cmd.png')


                        
#                os.system('echo seshan | sudo -S killall fbi')

#                os.system('echo seshan | sudo -S fbi -d /dev/fb0 -T 3 -noverbose -a cmd.png &')

#                for event in device.read_loop():
#                        if event.type == evdev.ecodes.EV_KEY:
#                                print(evdev.categorize(event))
#                                break

                
#                if int(red) >= ghostmax and int(red) > int(redold):
#                        broadcast("RESET")
#	        if int(blue) >= ghostmax and int(blue) > int(blueold):
#                        broadcast("RESET")
#
#	        if int(pac) >= pacmax and int(pac) > int(pacold): #TESTING AS 1 NOT 24
#                        broadcast("RESET")

                
        os.system('echo seshan | sudo -S killall fbi')

        os.system('echo seshan | sudo -S fbi -d /dev/fb0 -T 3 -noverbose -a cmd.png > /dev/null 2>&1 &')

        yelold = yel
        redold = red
        greenold = green


class Reset(object):
   global reset
   def __init__(self):
           print ("READING TOUCHSCREEN\n\n")

   def watch(self):
           global yelold,redold,greenold,need_reset,target,bkgPic,gameOver,yelWon,redWon,greenWon
           global reset,need_reset,locations,touchx,touchy
           btn_pressed = 0
           btn_processed = 0
           x = -1
           y = -1
           x_p = 0
           y_p = 0

           for event in device.read_loop():
#                print(evdev.categorize(event))
                if event.type == evdev.ecodes.EV_KEY:
                           if event.code == evdev.ecodes.BTN_TOUCH:
                                   if btn_pressed == 1:
                                           btn_pressed = 0
                                           btn_processed = 0
                                           print("RELEASED")
                                   else:
                                           btn_pressed = 1
                                           print("PRESSED")
                    
                if event.type == evdev.ecodes.EV_ABS:
                        if event.code == evdev.ecodes.ABS_MT_POSITION_X:
                                print("X: " + str(event.value))
                                x = event.value
                                if btn_pressed == 1:
                                        x_p = 1
                        if event.code == evdev.ecodes.ABS_MT_POSITION_Y:
                                print("Y: " + str(event.value))            
                                y = event.value
                                if btn_pressed == 1:
                                        y_p = 1

                        if x != -1 and y != -1 and btn_processed == 0 and btn_pressed == 1:
                                btn_processed = 1
                                print("X: " + str(x))
                                print("Y: " + str(y))  
                                touchx = x
                                touchy = y
                                if x > 390 and x < 620 and y > 360 and y < 450:
                                        print "Reset Pressed"
                                        reset = 1
                                        updatedata("Reset1")
                                        broadcast("RESET")
	                                os.system('echo seshan | sudo -S aplay win.wav &')
                                        reset = 0
                                        sleep(8)
                                        need_reset = 0
                                        print "Reset Done"
                                        updatedata("Reset")
                                elif x > 710 and x < 800 and y > 410 and y < 480:
                                        print("SWITCHING TO ENGLISH")
                                        bkgPic = "bkg-en.png"
                                        gameOver = "Game Over"
                                        yelWon = "Yellow Robot Wins"
                                        redWon = "Red Robot Wins"
                                        greenWon = "Orange Robot Wins"
                                        updatedata("Language")
                                elif x > 710 and x < 800 and y > 330 and y < 410:
                                        print("SWITCHING TO DANISH")
                                        bkgPic = enToDa["bkg-en.png"]
                                        gameOver = enToDa["Game Over"]
                                        yelWon = enToDa["Yellow Robot Wins"]
                                        redWon = enToDa["Red Robot Wins"]
                                        greenWon = enToDa["Orange Robot Wins"]
                                        updatedata("Language")
                                elif x > 710 and x < 800 and y > 275 and y < 330:
                                        print("SWITCHING TO DANISH")
                                        bkgPic = enToEs["bkg-en.png"]
                                        gameOver = enToEs["Game Over"]
                                        yelWon = enToEs["Yellow Robot Wins"]
                                        redWon = enToEs["Red Robot Wins"]
                                        greenWon = enToEs["Orange Robot Wins"]
                                        updatedata("Language")
                                else:
                                        updatedata("Touch")

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
	print "Active on port: " + str(port) + "\n"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            conn, addresstup = self.sock.accept()
	    address, tmp = addresstup
            threading.Thread(target = self.handleBot,args = (conn,address)).start()

    def handleBot(self, client, address):
#        global target
#        target = newTarget(possibleCols[0])
        global connections
        setmsgcolor = 1
        msgcolor = ''
#        print "HANDLE GHOST"
        while True:
            try:
                data = ''
                data_len_str= client.recv( struct.calcsize("!I") )
                data_len = (struct.unpack("!I", data_len_str))[0]
                while (data_len > 0):
                    data += client.recv( data_len )
                    data_len -= len(data)
		print data 
                if data:
                    botid = data.split(';')[0]
                    score = data.split(';')[1]
                    print("new connection req from: " + botid + " score: " + score + "\n")
                    if botid == '192.168.0.4':
                      msgcolor = "green"
                    elif botid == '192.168.0.6':
                      msgcolor = "red"
                    elif botid == '192.168.0.2':
                      msgcolor = "yellow"
                    elif botid == "10.42.0.1":
                      msgcolor = "spinner"
                    if setmsgcolor:
                            setmsgcolor = 0
                            connections.append((client, "G"+msgcolor))
                            send_str = str(str(target)).encode()
                            send_msg = struct.pack('!I', len(send_str))
                            send_msg += send_str
                            client.sendall(send_msg)

                    scores[msgcolor] = int(score)
#                   print str(locations) + ";" + str(scores["pacman"]) + ";" + str(scores["red"]) + ";" + str(scores["green"])
		    updatedata(msgcolor)
                else:
                    raise error('Tile disconnected')
            except Exception as e:
                print "GhostHandler Exception"
                print str(e.args)
                if setmsgcolor == 0:
                        connections = [i for i in connections if i[0] != client]
                        #filter(connections, lambda conn: conn[0] != client)
#                        connections.remove((client, self.botcolor + " ghost"))
                client.close()
		updatedata(msgcolor)
                return False


#            except:
#                #client.close()
#                return False

updatedata("main")
os.system('echo seshan | sudo -S aplay win.wav &')
Resetter = Reset()
threading.Thread(target = Resetter.watch).start()
        
if __name__ == "__main__":
#    tileServer = ThreadedServer('',5000)
#    threading.Thread(target = tileServer.listen).start()
    ThreadedServer('',6000).listen()


