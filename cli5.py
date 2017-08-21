import socket
import sys
import logging

LOG_FILENAME = 'CL.log'
logF = '%(asctime)s- %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=LOG_FILENAME, format=logF, level=logging.DEBUG)
logging.info('wake_program')
  
def main():
    host = 'localhost'
    port = 4649
    bufsize = 4096
    select_num = 10
 
    logging.info('menu')
    print('-----------------------------------------------------')
    print('')
    print('何をしますか？')
    print('')

select_num = input('1.新規登録  2.参照  3.削除 4.プログラムの終了 5.サーバーの終了') 
    print('')
    print('-----------------------------------------------------') 
    if select_num == '4':
        print('本当に終了しますか？')
        num =input('1.はい　,2.いいえ')
        if num == '1':
            print('プログラムを終了します。')
            logging.info('sleep_program')            
            sys.exit()
 
        else :
            print('メニュー画面に戻ります')
            return main()
 
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
    except:
        print('ソケットの通信が切断されています。')
        logging.info('sleep_program')
        sys.exit()
 
    sock.send(select_num.encode('utf-8'))
    if select_num == '1':
        logging.info('select_regist')
        print('新規登録が選ばれました')        
        Key = input('Keyを入力してください:')
        sock.send(Key.encode('utf-8'))
        Value = input('Valueを入力してください:')
        sock.send(Value.encode('utf-8'))        
        print('')
        print('[Key]= %s , [Value]= %s ' % (Key, Value))
        print('登録完了しました!')
        logging.info('regist_comp')
        print('')
        return main()
 
 
    elif select_num == '2':
        logging.info('select_refer')
        print('参照が選ばれました')
        print('')
        Key = input('Keyを入力してください:')
        print('')
        sock.send(Key.encode('utf-8'))
 
        msg = sock.recv(bufsize)
 
        print('[Key]= %s の [Value]の値は%sです。' % (Key, msg.decode('utf-8')))
        logging.info('refer_comp')
        print('')
        return main()
        
    elif select_num == '3':
        logging.info('select_del')
        print('削除が選ばれました')
        print('')
        Key = input('Keyを入力してください:')
        print('')
        sock.send(Key.encode('utf-8'))
 
        err = sock.recv(bufsize)
 
        if (err.decode('utf-8')) == '1':
            print('[Key]= %s は削除されました' % (Key))
            logging.info('del_comp')
            return main()
 
        if (err.decode('utf-8')) == '0':
            print('そのようなKeyは存在しておりません')
            logging.info('del_miss')
            return main()
 
    elif select_num == '4':
        print('本当に終了しますか？')
        num =input('1.はい　,2.いいえ')
        if num == '1':
            print('プログラムを終了します。')
            logging.info('sleep_program')
            sys.exit()

        else :
            print('メニュー画面に戻ります')
            return main()

    elif select_num == '5':
        print('サーバーを終了します。')
        logging.info('sleep_server')
        sys.exit()


    else:
        print('選択肢の中から選んでください。')
        return main()


if __name__ == '__main__':
    main()
