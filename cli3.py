#170816

import socket
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
    bufsize3 = 4096    bufsize4 = 4096
    bufsize5 = 4096
    s = 10
    san = 100
 
    print('-----------------------------------------------------')    print('')
    print('何をしますか？')
    print('')
    s = input('1.新規登録  2.参照  3.削除 4.プログラムの終了')
    print('')
    print('-----------------------------------------------------')
 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.send(s.encode('utf-8'))
 
    if s == '1':
        print('新規登録が選ばれました')
        Key = input('Keyを入力してください:')
        sock.send(Key.encode('utf-8'))
        Value = input('Valueを入力してください:')
        sock.send(Value.encode('utf-8'))
        print('')
        print('[Key]= %s , [Value]= %s ' % (Key, Value))
        print('登録完了しました!')
        print('')
        return main()
 
 
    elif s == '2':
        print('参照が選ばれました')
        print('')
        Key2 = input('Keyを入力してください:')
        print('')
        sock.send(Key2.encode('utf-8'))
        syo = sock.recv(san)

        print('[Key]= %s の [Value]の値は%sです。' % (Key2, syo.decode('utf-8')))
        print('')
        return main()
 
    elif s == '3':
        print('削除が選ばれました')
        print('')
        Key3 = input('Keyを入力してください:')
        print('')
        sock.send(Key3.encode('utf-8'))
        print('[Key]= %s は削除されました' % (Key3))
        return main()
 
    elif s == '4':
        print('本当に終了しますか？')
        e =input('1.はい　,2.いいえ')
        if e == '1':
            print('プログラムを終了します。')
            sys.exit()
 
        else :
            print('メニュー画面に戻ります')
            return main()
 
 
    else:
        print('選択肢の中から選んでください。')
        return main()
 
 
if __name__ == '__main__':
    main()
