import socket
import sys

MAX_BUF = 2048
SERV_PORT = 50000
isConnected = False

while True:
  line = input('> ')
  temp = line.split(' ')
  command = temp[0]
  if temp[2][0] is not '/':
    temp[2] = '/' + temp[2]
  if command == 'subscribe' and len(temp) == 3:
    broker_ip = temp[1]
    sentmsg = temp[0] + '?' + temp[2] + '?'
  elif command == 'publish':
    if len(temp) > 3:
      broker_ip = temp[1]
      sentmsg = temp[0] + '?' + temp[2] + '?' + ' '.join(temp[3:])
    else:
      print('No data')
  else:
    print('Command does not exist')

  if not isConnected:
    addr = (broker_ip, SERV_PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    isConnected = True
  s.send(sentmsg.encode('utf-8'))

  while True and command == 'subscribe':
    modifiedMsg = s.recv(2048)
    print (modifiedMsg.decode('utf-8'))
s.close()
