import socket
import sys

MAX_BUF = 2048
SERV_PORT = 50000

addr = ('localhost', SERV_PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(addr)

username = input('Enter your name: ')
while True:
  txtout = input('%s> ' %username)
  sentmsg = username + '> ' + txtout
  s.send(sentmsg.encode('utf-8'))
  if txtout == 'quit':
    break
  modifiedMsg = s.recv(2048)
  print (modifiedMsg.decode('utf-8'))

s.close()
