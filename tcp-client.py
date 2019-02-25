import socket
import sys
import time

MAX_BUF = 2048
SERV_PORT = 50000

while True:
  try:
    line = input('COMMAND> ')
    temp = line.split(' ')
    command = temp[0]
    if temp[2][0] is not '/':
      temp[2] = '/' + temp[2]
    if command == 'subscribe' and len(temp) == 3:
      broker_ip = temp[1]
      sentmsg = command + '?' + temp[2] + '?'
    elif command == 'publish':
      if len(temp) > 3:
        broker_ip = temp[1]
        sentmsg = command + '?' + temp[2] + '?' + ' '.join(temp[3:])
      else:
        print('No data')
    else:
      print('Command does not exist')

    addr = (broker_ip, SERV_PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if command == 'publish':
      s.settimeout(1)
    s.connect(addr)
    isConnected = True
    s.send(sentmsg.encode('utf-8'))
    
    while True:
      modifiedMsg = s.recv(2048)
      print ('RESPONSE> ', modifiedMsg.decode('utf-8'))
      if command == 'publish':
        break
    
    while True and command == 'publish':
      data = input('DATA> ')
      if data == 'quit':
        s.close()
        break
      sentmsg = command + '?' + temp[2] + '?' + data
      s.send(sentmsg.encode('utf-8'))
  except:
    print('Socket timeout')
s.close()
