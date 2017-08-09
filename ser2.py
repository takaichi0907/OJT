import socket
import redis
import logging
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
    bufsize2 = 4096
    bufsize3 = 4096
    bufsize4 = 4096
    s = 10
    func = 10
    san = 100
 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(backlog)
    print('Waiting for connections...')
    while True:
               conn, address = sock.accept() # 要求が来るまでブロック
 
               func = conn.recv(s)
               print(func.decode('utf-8'))
 
               if (func.decode('utf-8')) == '1':
                         msg = conn.recv(bufsize)
                         print(msg.decode('utf-8'))
                         msg2 = conn.recv(bufsize2)
                         print(msg2.decode('utf-8'))
                         r.set(msg, msg2)
 
               elif (func.decode('utf-8')) == '2':
                         msg3 = conn.recv(bufsize3)
                         print(msg3.decode('utf-8'))
                         san = r.get(msg3)
                         print(san.decode('utf-8'))
 
                         sock.send(san.encode('utf-8'))
 
 
               elif (func.decode('utf-8')) == '3':
                         msg4 = conn.recv(bufsize4)
                         print(msg4.decode('utf-8'))
                         r.delete(msg4)
 
               else:
                         print('失敗')
 
 if __name__ == '__main__':
      main()
