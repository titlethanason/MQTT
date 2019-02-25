import socket
import traceback
from threading import Thread
import os,sys

SERV_PORT = 50000
listOfTopic = []

class sub_topic():
  def __init__(self):
    self.name : str = None
    self.subscribers = []
    self.data = []

def handle_client(s, ip):
  while True:
    txtin = s.recv(2048).decode('utf-8')
    print(ip + '> ' + txtin)
    command, topic, data = txtin.split('?')
    if command == 'subscribe':
      if not listOfTopic:
        temp = sub_topic()
        temp.name = topic
        temp.subscribers.append(s)
        listOfTopic.append(temp)
        print('Created ' + topic + ' as a new topic')
      else:
        topicExists = False
        for x in listOfTopic:
          if x.name == topic:
            x.subscribers.append(s)
            topicExists = True
            break
        if not topicExists:
          temp = sub_topic()
          temp.name = topic
          temp.subscribers.append(s)
          listOfTopic.append(temp)
          print('Created ' + topic + ' as a new topic')
      txtout = 'You have subscribed to ' + topic
      s.send(txtout.encode('utf-8'))
    elif command == 'publish':
      for x in listOfTopic:
        print(x.subscribers)
        if x.name == topic:
          for y in x.subscribers:
            y.send(data.encode('utf-8'))
    else:
      txtout = 'Sorry, ' + command + ' does not exist'
      s.send(txtout.encode('utf-8'))
  s.close()

def main():
  addr = ('localhost', SERV_PORT)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(addr)
  s.listen(5)
  print ('TCP threaded server started...')

  while True:
    sckt, addr = s.accept()
    try:
      sender_addr = str(addr[0]) + ':' + str(addr[1])
      print ('New client connected from ' + sender_addr)
      Thread(target=handle_client, args=(sckt,sender_addr,)).start()
    except:
      try:
        raise TypeError("Again !?!")
      except:
        pass
      traceback.print_exc()

  s.close()

if __name__ == '__main__':
   try:
     main()
   except KeyboardInterrupt:
     print ('Interrupted..')
     try:
       sys.exit(0)
     except SystemExit:
       os._exit(0)
