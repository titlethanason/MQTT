import socket
import traceback
from threading import Thread
import os,sys

SERV_PORT = 50000

def handle_client(s, ip):
  while True:
    txtin = s.recv(2048).decode('utf-8')
    print(ip + '> ' + txtin)
    if txtin == 'quit':
      print('**ANNOUNCEMENT: ' + ip + ' HAS DISCONNECTED**')
      break
    else:
      txtout = 'Sorry, ' + txtin + ' does not exist'
      s.sendto(txtout.encode('utf-8'), (ip.split(':')[0], int(ip.split(':')[1])))
  s.close()
  return

def main():
  addr = ('localhost', SERV_PORT)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(addr)
  s.listen(5)
  print ('TCP threaded server started ...')

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
     print ('Interrupted ..')
     try:
       sys.exit(0)
     except SystemExit:
       os._exit(0)

class sub_topic():
  def __init__(self):
    self.name : str = None
    self.subscribers = []
    self.data = []
