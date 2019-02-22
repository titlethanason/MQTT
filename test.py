from socket import * 
import sys

MAX_BUF = 2048
SERV_PORT = 50000

addr = ('localhost', SERV_PORT)
s = socket(AF_INET, SOCK_STREAM)
s.connect(addr)

username = input('Enter your name: ')
print ('%s> ' %(username), end='') 
sys.stdout.flush()
txtout = sys.stdin.readline().strip()
s.send(txtout.encode('utf-8'))
s.close()