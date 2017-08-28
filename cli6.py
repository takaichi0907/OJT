#170823
import socket
import sys
import logging
LOG_FILENAME = 'CL.log'
logF = '%(asctime)s- %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=LOG_FILENAME, format=logF, level=logging.DEBUG)

logging.info('プログラムが起動しました')

def main():
    host = 'localhost'
    port = 4649
    bufsize = 4096
    select_num = 10

    logging.info('メニュー画面を開きました')

    print('-----------------------------------------------------')
    print('')
    print('何をしますか？')
    print('')
    select_num = input(' 1.新規登録 \n 2.参照 \n 3.削除 \n 4.プログラムの終了 \n 5.サーバーの終了 \n 6.Redis内データ全削除 \n 7.[Key]一覧表示 \n 8.更新 \n→')
    print('')
    print('-----------------------------------------------------')

    if select_num == '4':
        print('本当に終了しますか？')
        num =input(' 1.はい \n 2.いいえ \n →')
        if num == '1':
            print('プログラムを終了します。')

            logging.info('プログラムが終了しました')

            sys.exit()

        else :
            print('メニュー画面に戻ります')
            return main()

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except:
        print('ソケットの通信が切断されています。')

        logging.info('プログラムが終了しました')

        sys.exit()

    sock.send(select_num.encode('utf-8'))
    if select_num == '1':

        logging.info('新規登録が選ばれました。')

        print('新規登録が選ばれました')
        Key = input('Keyを入力してください:')
        sock.send(Key.encode('utf-8'))
        Value = input('Valueを入力してください:')
        sock.send(Value.encode('utf-8'))
        print('')
        print('[Key]= %s , [Value]= %s ' % (Key, Value))
        print('登録完了しました!')

        logging.info('[Key]= %s , [Value]= %s の登録完了' % (Key, Value))

        print('')
        return main()


    elif select_num == '2':

        logging.info('参照が選ばれました')

        print('参照が選ばれました')
        print('')
        Key = input('Keyを入力してください:')
        print('')
        sock.send(Key.encode('utf-8'))

        Value = sock.recv(bufsize)

        print('[Key]= %s の [Value]の値は%sです。' % (Key, Value.decode('utf-8')))

        logging.info('[Key]= %s の [Value]= %sの参照完了。' % (Key, Value.decode('utf-8')))

        print('')
        return main()

    elif select_num == '3':

        logging.info('削除が選ばれました')

        print('削除が選ばれました')
        print('')
        Key = input('Keyを入力してください:')
        print('')
        sock.send(Key.encode('utf-8'))

        err = sock.recv(bufsize)

        if (err.decode('utf-8')) == '1':
            print('[Key]= %s は削除されました' % (Key))

            logging.info('[Key]= %s は削除完了' % (Key))

            return main()

        if (err.decode('utf-8')) == '0':
            print('そのようなKeyは存在しておりません')
            logging.info('削除に失敗しました')
            return main()

    elif select_num == '4':
        print('本当に終了しますか？')
        num =input(' 1.はい \n 2.いいえ \n →')
        if num == '1':
            print('プログラムを終了します。')

            logging.info('プログラムが終了しました')

            sys.exit()

        else :
            print('メニュー画面に戻ります')
            return main()

    elif select_num == '5':
        print('サーバーを終了します。')

        logging.info('サーバーが終了しました')

        sys.exit()

    elif select_num == '6':
        print('本当に全削除しますか？')
        num = input(' 1.はい \n 2.いいえ \n →')
        if num == '1':
            print('OK')
            sock.send(num.encode('utf-8'))

            logging.info('Redisデータ全削除完了')

            return main()

        else:
            sock.send(num.encode('utf-8'))
            print('メニュー画面に戻ります')
            return main()

    
    elif select_num == '7':
        print('[Key]一覧表示します')

        logging.info('[Key]一覧表示')

        Keys = sock.recv(bufsize)
        R = Keys.split("/")
        print(str(R)) #.decode('utf-8'))

        logging('[Key]の一覧表示完了')
        
    elif select_num == '8':
        print('更新します')
        Key = input('更新したいKeyを入力してください \n →')
        sock.send(Key.encode('utf-8'))

        refer_value = sock.recv(bufsize)



        print('[Key]= %s の [Value]の値は%sです。' % (Key, refer_value.decode('utf-8')))

        print('更新しますか？')
        num = input(' 1.はい \n 2.いいえ \n →')

        if num == '1':
            #Update_Key = input('Keyを入力してください:')
            #sock.send(Update_Key.encode('utf-8'))
            Update_Value = input('Valueを入力してください:')
            sock.send(Update_Value.encode('utf-8'))
            print('')
            print('[Key]= %s , [Value]= %s ' % (Key, Update_Value))
            print('更新が完了しました')

            logging.info('更新が完了しました')

        else :
            print('メニュー画面に戻ります')
            return main()

    else:
        print('選択肢の中から選んでください。')
        return main()


if __name__ == '__main__':
    main()
