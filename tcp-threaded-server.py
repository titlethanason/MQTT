
from socket import * 
from threading import Thread
import os,sys

SERV_PORT = 50000

def handle_client(s):
  while True:
    try:
      txtin = s.recv(1024)
      print ('Client> %s' %(txtin.encode('utf-8')))
      if txtin == b'quit':
          print('Client disconnected ...')
          break
      else:
          txtout = txtin.upper()    
          s.send(txtout)
    except Exception as e:
      print(str(e))
      break
  s.close()
  return

def main():
  addr = ('localhost', SERV_PORT)
  s = socket(AF_INET, SOCK_STREAM)
  s.bind(addr)
  s.listen(5)
  print ('TCP threaded server started ...')

  while True:
    sckt, addr = s.accept()
    ip, port = str(addr[0]), str(addr[1]) 
    print ('New client connected from ..' + ip + ':' + port)
  
    try:
      Thread(target=handle_client, args=(sckt,)).start()
    except:
      print("Cannot start thread..")
      import traceback
      trackback.print_exc()

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
