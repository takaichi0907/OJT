#170816

import socket
import redis
from contextlib import closing

import logging
LOG_FILENAME = 'ser.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
logging.debug('This message should go to the log file')

r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

def main():
    host = 'localhost'
    port = 4649
    backlog = 10
    bufsize = 4096
    s = 100
    func = 10
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    readfds = set([sock])
    try:
       sock.bind((host, port))
       sock.listen(backlog)
       print('Waiting for connections...')
       while True:
             conn, address = sock.accept() # 要求が来るまでブロック
 
             func = conn.recv(s)
             print(func.decode('utf-8'))
             
             if (func.decode('utf-8')) == '1':
                           print('新規登録')
                           msg = conn.recv(bufsize)
                           print(msg.decode('utf-8'))
                           msg2 = conn.recv(bufsize2)
                           print(msg2.decode('utf-8'))
                           r.set(msg, msg2)
  
             elif (func.decode('utf-8')) == '2':
                           print('参照')
                           msg3 = conn.recv(bufsize3)
                           print(msg3.decode('utf-8'))
                           san = r.get(msg3)
                           print(san.decode('utf-8'))
                           conn.send(san)
 
 
             elif (func.decode('utf-8')) == '3':
                           print('削除')
                           msg4 = conn.recv(bufsize4)
                           print(msg4.decode('utf-8'))
                           r.delete(msg4)
 
             elif (func.decode('utf-8')) == '4':
                           print('プログラムの終了')
 
 
    finally:
       for sock in readfds:
             sock.close()
    return

if __name__ == '__main__':
     main()
