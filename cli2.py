import socket
import logging
from contextlib import closing
import sys
import logging
LOG_FILENAME = 'cli.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

logging.debug('This message should go to the log file')

def main():
    host = 'localhost'
    port = 4649
    bufsize = 4096
    bufsize2 = 4096 
    bufsize3 = 4096
    bufsize4 = 4096
    bufsize5 = 4096
    s = 10
    san = 10
 
 
    print('何をしますか？')
    s = input('1.新規登録  2.参照  3.削除 4.プログラムの終了')
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.send(s.encode('utf-8'))
 
    if s == '1':
         print('新規登録が選ばれました')
         Key = input('Keyを入力してください:')
         sock.send(Key.encode('utf-8'))
         Value = input('Valueを入力してください:')
         sock.send(Value.encode('utf-8'))
         print('登録完了しました!') 
         return main()
 
 
    elif s == '2':
         print('参照が選ばれました')
         Key2 = input('Keyを入力してください:')
         sock.send(Key2.encode('utf-8'))
 
         syo = conn.recv(bufsize5)
         print(syo.decode('utf-8'))
         return main()
 
    elif s == '3':
         print('削除が選ばれました')
         Key3 = input('Keyを入力してください:')
         sock.send(Key3.encode('utf-8'))
         print('削除完了しました!')
         return main()
         
    elif s == '4':
         print('本当に終了しますか？')
         e =input('1.はい　,2.いいえ')
         if e == '1':
            input('プログラムを終了します。')
            sys.exit()
 
         elif e == '2':
            print('メニュー画面に戻ります')
            return main()
 
    else:
         print('選択肢の中から選んでください。')
         return main()
 
 if __name__ == '__main__':
      main()
