import socket
import redis
import logging
from contextlib import closing

r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

 
def main():
    host = 'localhost'
    port = 4649
    backlog = 10
    bufsize = 4096
    bufsize2 = 4096
#   bufsize3 = 4096
#   bufsize4 = 4096
 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with closing(sock):
         sock.bind((host, port))
         sock.listen(backlog)
         print('Waiting for connections...')
         while True:
               conn, address = sock.accept()
               with closing(conn):
                    func = conn.recv(s)
                    print(func)
 
                    if func ==1:
                        msg = conn.recv(bufsize)
                        print(msg.decode('utf-8'))
                        conn.send(msg)
                        msg2 = conn.recv(bufsize2)
                        print(msg2.decode('utf-8'))
                        conn.send(msg2)
                        r.set(msg, msg2)

                    elif func == 2:
                        msg3 = conn.recv(bufsize3)
                        print(msg3.decode('utf-8'))
                        conn.send(msg3)
                        r.get(msg3)
                
                    elif func == 3:
                        msg4 = conn.recv(bufsize4)
                        print(msg4.decode('utf-8'))
                        conn.send(msg4)
                        r.delete(msg4)
 
 
 
if __name__ == '__main__':
     main()
