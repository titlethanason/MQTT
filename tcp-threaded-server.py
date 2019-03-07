import socket
import traceback
import threading
import os,sys

SERV_PORT = 50000

class sub_topic():
  def __init__(self, name):
    self.name = name
    self.subscribers = []
    self.child = []
  def addSub(self, path, sckt):
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
    else:
      self.subscribers.append(sckt)
  def sendData(self,path,data):
    pathExists = False
    if len(path) > 1:
      for x in self.child:
        if x.name == path[1]:
          pathExists = x.sendData(path[1:], data)
        elif path[1] == '#':
          pathExists = x.sendData(path[1:], data)
        elif path[1] == '+':
          pathExists |= x.sendData(path[1:], data)
    else:
      if len(self.subscribers) > 0:
        pathExists = True
        for x in self.subscribers:
          x.send(data.encode('utf-8'))
      if path[0] == '#':
        for x in self.child:
          pathExists |= x.sendData('#', data)
    return pathExists
  def removeSub(self, path, sckt):
    if len(path) > 1:
      for x in self.child:
        if x.name == path[1]:
          x.removeSub(path[1:], sckt)
    else:
      self.subscribers.remove(sckt)

rootOfTopics = sub_topic('root')

def handle_client(s, ip):
  checkPublisher = None
  try:
    while True:
      txtin = s.recv(2048).decode('utf-8')
      command, topic, data = txtin.split('?')
      print(ip + '> ' + txtin)
      checkPublisher = command
      path = topic.split('/')
      if command == 'subscribe':
        rootOfTopics.addSub(path, s)
        print('Created ' + topic + ' as a new topic')
        txtout = 'You have subscribed to ' + topic
        print('Message sent: ' + txtout)
        s.send(txtout.encode('utf-8'))
      elif command == 'publish':
        foundTopic = rootOfTopics.sendData(path,data)
        if foundTopic:
          txtout = 'Sent data to all subsribers'
          print('Message sent: ' + txtout)
          s.send(txtout.encode('utf-8'))
        else:
          txtout = 'Topic does not exist or no subscriber in the topic'
          print('Message sent: ' + txtout)
          s.send(txtout.encode('utf-8'))
      else:
        txtout = 'Sorry, ' + command + ' does not exist'
        print('Message sent: ' + txtout)
        s.send(txtout.encode('utf-8'))
  except (socket.error, ValueError):
    if checkPublisher != 'publish':
      rootOfTopics.removeSub(path, s)
      print(ip + ' has been removed from ' + '/'.join(str(x) for x in path))
    else:
      print(ip + ' has disconnected from the broker')
  except:
    traceback.print_exc()
  print('Thread:' + str(threading.get_ident()) + ' is closing...')
  s.close()

def main():
  addr = ('localhost', SERV_PORT)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(addr)
  s.listen(10)
  print ('MQTT Broker started...')

  while True:
    sckt, addr = s.accept()
    try:
      sender_addr = str(addr[0]) + ':' + str(addr[1])
      print ('New client connected from ' + sender_addr)
      threading.Thread(target=handle_client, args=(sckt,sender_addr,)).start()
    except:
      print('Could not start a thread..')
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
