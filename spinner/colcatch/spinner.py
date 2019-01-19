#!/usr/bin/python3

# Echo server program
import socket,time,os,struct,threading
import ev3dev.ev3 as ev3
from time import sleep

motor = ev3.LargeMotor('outB')
motor.reset()
motor.stop_action = "brake"

ip = socket.gethostbyname(socket.gethostname())
cc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cc_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

score = 0
findCol = "green"

colToInt = ["none","black","blue","green","yellow","red","white","brown"]

colIntToDeg = [0,240,180,60,120,300,0,0]


print("INIT")

class ControlChannel(object):
   global cc_sock,score
   def __init__(self):
       self.host = '10.42.0.3'    # The remote host
       self.port = 6000             # The same port as used by the server
       print ("Active on port: 6000")

   def control(self, data):
       print("DATA: "+data)
       global score, findCol
       time.sleep(1)
       print(data)
       if "RESET" in data:
          print("resetting")
          score = 0
          self.sendscore(score)
       elif data in str(colToInt):
          findCol = data

   def watch(self):
      global cc_sock, score
      cc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      cc_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
      try:
          cc_sock.connect((self.host, self.port))
          print("Connected! to " + self.host)
      except:
          pass
      while True:
         data = ''
         try: 
            data_len_str= cc_sock.recv( struct.calcsize("!I") )
            data_len = (struct.unpack("!I", data_len_str))[0]
            while (data_len > 0):
               data += cc_sock.recv( data_len ).decode()
               data_len -= len(data)
            print(data)
            self.control(data)
         except Exception as e:
            print("FAILURE TO RECV.." + str(e.args) + "..RECONNECTING")
            try:
               cc_sock.close()
               cc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
               cc_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
               cc_sock.connect((self.host, self.port))
               print("Connected! to " + self.host)
               self.sendscore(score)
            except:
               sleep(2)
               pass
           # threading.Thread(target = self.control,args = (str(msg))).start()

   def sendscore(self,value):
       global cc_sock
       send_str = str(ip + ";" + str(value)).encode()
       send_msg = struct.pack('!I', len(send_str))
       send_msg += send_str
       print("sending " + str(len(send_str)) + " bytes")
       print("sending total " + str(len(send_msg)) + " bytes")
       print("sending " + str(send_msg))
       try:
           cc_sock.sendall(send_msg)
           print("SENDING COMPLETE")
           #      data = s.recv(1024)
       except Exception as e:
           print("FAILURE TO SEND.." + str(e.args) + "..RECONNECTING")
           try:
               cc_sock.connect((self.host, self.port))
               print("connected to " + self.host)
               print("sending " + send_msg)
               cc_sock.sendall(send_msg)
           except:
               sleep(2)
               pass

          
Server = ControlChannel()
threading.Thread(target = Server.watch).start()
sleep(1)
Server.sendscore(0)
pac_count = 0
lastDeg = 0
while True:
     print("Find: "+str(colToInt.index(findCol))+" Deg: "+str(colIntToDeg[colToInt.index(findCol)]) + " Cur Deg: " + str(motor.position))
#     if colIntToDeg[colToInt.index(findCol)] != lastDeg:
     if abs(motor.position-colIntToDeg[colToInt.index(findCol)]) > 4:
         i = 0
         while i < 5:
           if motor.position < colIntToDeg[colToInt.index(findCol)]:
              motor.run_to_abs_pos(speed_sp=100, position_sp=colIntToDeg[colToInt.index(findCol)])
           else:
              motor.run_to_abs_pos(speed_sp=-100, position_sp=colIntToDeg[colToInt.index(findCol)])
           i = i+1
     lastDeg = colIntToDeg[colToInt.index(findCol)]
