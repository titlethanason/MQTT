import socket
import traceback
from threading import Thread
import os,sys

SERV_PORT = 50000

class sub_topic():
  def __init__(self, name):
    self.name = name
    self.subscribers = []
    self.child = []
  def addSub(self, path, sckt):
    self.subscribers.append(sckt)
    childExists = False
    if len(path) > 1:
      for x in self.child:
        if x.name == path[1]:
          x.addSub(path[1:], sckt)
          childExists = True
          break
      if not childExists:
        child = sub_topic(path[1])
        child.addSub(path[1:], sckt)
        self.child.append(child)
  def sendData(self,path,data):
    pathExists = False
    if len(path) > 1:
      for x in self.child:
        if x.name == path[1]:
          pathExists = x.sendData(path[1:], data)
    else:
      if len(self.subscribers) > 0:
        pathExists = True
        for x in self.subscribers:
          x.send(data.encode('utf-8'))
    return pathExists
  def removeData(self, path, sckt):
    self.subscribers.remove(sckt)
    print('Removed socket in ' + path[0])
    if len(path) > 1:
      for x in self.child:
        if x.name == path[1]:
          x.removeData(path[1:], sckt)

rootOfTopics = sub_topic('root')

def handle_client(s, ip):
  checkPublisher = None
  try:
    while True:
      txtin = s.recv(2048).decode('utf-8')
      print(ip + '> ' + txtin)
      command, topic, data = txtin.split('?')
      checkPublisher = command
      path = topic.split('/')
      if command == 'subscribe':
        rootOfTopics.addSub(path, s)
        print('Created ' + topic + ' as a new topic')
        txtout = 'You have subscribed to ' + topic
        s.send(txtout.encode('utf-8'))
      elif command == 'publish':
        foundTopic = rootOfTopics.sendData(path,data)
        if foundTopic:
          s.send('Sent data to all subsribers'.encode('utf-8'))
        else:
          s.send('Topic does not exist'.encode('utf-8'))
      else:
        txtout = 'Sorry, ' + command + ' does not exist'
        s.send(txtout.encode('utf-8'))
  except:
    if checkPublisher != 'publish':
      rootOfTopics.removeData(path, s)
    else:
      print(ip + ' has disconnected from the broker')
  s.close()

def main():
  addr = ('localhost', SERV_PORT)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(addr)
  s.listen(5)
  print ('TCP threaded server started...')

  while True:
    sckt, addr = s.accept()
    sender_addr = str(addr[0]) + ':' + str(addr[1])
    print ('New client connected from ' + sender_addr)
    Thread(target=handle_client, args=(sckt,sender_addr,)).start()

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
