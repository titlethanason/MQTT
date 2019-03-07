import socket
import sys

MAX_BUF = 2048
SERV_PORT = 50000

while True:
  try:
    line = input('COMMAND> ')
    temp = line.split(' ')
    command = temp[0]
    correctFormat = False
    if command == 'subscribe' or command == 'publish':
      while not correctFormat:
        if command == 'subscribe' and len(temp) > 2:
          correctFormat = True
          data = ''
        elif command == 'publish' and len(temp) > 3:
          correctFormat = True
          data = ' '.join(temp[3:])
        else:
          if len(temp) == 1:
            temp = temp + input('     IP> ').split(' ')
          elif len(temp) == 2:
            temp = temp + input('  TOPIC> ').split(' ')
          elif len(temp) == 3:
            temp = temp + input('   DATA> ').split(' ')
      if len(temp) > 3 and command == 'subscribe':
        print('Oversized length of the subscribe command')
        raise ValueError
    else:
      print('Command does not exist')
      raise ValueError

    broker_ip = temp[1]
    if temp[2][0] != '/':
      temp[2] = '/' + temp[2]
    sendmsg = command + '?' + temp[2] + '?' + data

    addr = (broker_ip, SERV_PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      s.connect(addr)
    except:
      print('Connection error..\nCould not connect to the broker. Please check broker_ip.')
      raise socket.error
    
    s.send(sendmsg.encode('utf-8'))

    while True:
      modifiedMsg = s.recv(2048)
      print ('RESPONSE> ', modifiedMsg.decode('utf-8'))
      if 'does not exist' in modifiedMsg.decode('utf-8'):
        s.close()
        break
      if command == 'publish':
        data = input('DATA> ')
        if data == 'quit':
          s.close()
          break
        sendmsg = command + '?' + temp[2] + '?' + data
        s.send(sendmsg.encode('utf-8'))

  except socket.error:
    s.close()
  except ValueError:
    pass
s.close()
