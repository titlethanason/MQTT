import socket
import sys

MAX_BUF = 2048
SERV_PORT = 50000

line = input('> ')
temp = line.split(' ')
command = temp[0]
if command == 'subscribe' and len(temp) == 3:
  broker_ip = temp[1]
  sentmsg = temp[0] + '?' + temp[2]
elif command == 'publish' and len(temp) == 4:
  broker_ip = temp[1]
  sentmsg = temp[0] + '?' + temp[2] + '?' + temp[3]
else:
  print('Subscribe to Pewdiepie, dude')

addr = (broker_ip, SERV_PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(addr)
s.send(sentmsg.encode('utf-8'))

while True:
  modifiedMsg = s.recv(2048)
  print (modifiedMsg.decode('utf-8'))

s.close()
