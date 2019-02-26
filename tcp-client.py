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
    if command == 'subscribe':
      while len(temp) < 3:
        temp.append(input('       > '))
      data = ''
    elif command == 'publish':
      while len(temp) < 4:
        temp.append(input('       > '))
      data = ' '.join(temp[3:])
    else:
      print('Command does not exist')

    broker_ip = temp[1]
    if temp[2][0] != '/':
      temp[2] = '/' + temp[2]
    sendmsg = command + '?' + temp[2] + '?' + data

    addr = (broker_ip, SERV_PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if command == 'publish':
      s.settimeout(1)
    try:
      s.connect(addr)
    except:
      print('Connection error..\nCould not connect to the broker. Please check broker_ip.')
      raise socket.error

    s.send(sendmsg.encode('utf-8'))

    while True:
      modifiedMsg = s.recv(2048)
      print ('RESPONSE> ', modifiedMsg.decode('utf-8'))
      if command == 'publish':
        data = input('DATA> ')
        if data == 'quit':
          s.close()
          break
        sendmsg = command + '?' + temp[2] + '?' + data
        s.send(sendmsg.encode('utf-8'))

  except socket.error:
    print('hi')
    s.close()
s.close()
