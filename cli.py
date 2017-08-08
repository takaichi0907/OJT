import socket
import logging
from contextlib import closing

"""
def funcon(s):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with closing(sock):
         sb = s
         sock.connect((host, port))
         sock.send(sb.encode('utf-8'))
"""
 
 
def main():
    host = 'localhost'
    port = 4649
    bufsize = 4096
    bufsize2 = 4096

    print('何をしますか？'
    s = input('1.新規登録  2.参照  3.削除')
 
    #    funcon(s)
 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with closing(sock):
         sock.connect((host, port))
         sb = s
         sock.send(sb.encode('utf-8'))
  
         if s == '1':
              print('新規登録が選ばれました')
 
              sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
              with closing(sock):
                   sock.connect((host, port))
                   Key = input('Key:')
                   sock.send(Key.encode('utf-8'))
                   print(sock.recv(bufsize).decode('utf-8'))
                   print('k-in')
                   Value = input('Value:')                   print('v1')
                   sock.send(Value.encode('utf-8'))
                   print('v2')
                   print(sock.recv(bufsize2).decode('utf-8'))
                   print('v-in')
                   print('登録完了しました!')
         #        return
 
 
 
 
         elif s == '2':
                print('参照が選ばれました')
 
                host = 'localhost'
                port = 4649
                bufsize3 = 4096
 
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                with closing(sock):
                     sock.connect((host, port))
                     sock.send(sb.encode('utf-8'))
                     Key2 = input('Key2:')
                     sock.send(Key2.encode('utf-8'))
                     print(sock.recv(bufsize3).decode('utf-8'))
 
 
 
         elif s == '3':
                print('削除が選ばれました')
 
                host = 'localhost'
                port = 4649
                bufsize4 = 4096
   
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                with closing(sock):
                     sock.connect((host, port))
                     sock.send(sb.encode('utf-8'))
                     Key3 = input('Key3:')
                     sock.send(Key3.encode('utf-8'))
                     print(sock.recv(bufsize4).decode('utf-8'))
                     print('削除完了しました!')
   
         elif s == '4':
                print('プログラムを終了します')
   
         else:
                print('もう一度やり直してください')
   
    if __name__ == '__main__':
         main()
