#0830

import socket
import sys
import time
import logging



LOG_FILENAME = 'CL.log'
logF = '%(asctime)s- %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=LOG_FILENAME, format=logF, level=logging.DEBUG)

argPort = sys.argv

logging.info('プログラムが起動しました')

def main():
    host = 'localhost'
    if len(argPort) == 1:
        port = 4649
    else :
        port = int(argPort[1])
    bufsize = 4096
    Menu = 10

    logging.info('メニュー画面を開きました')

    print("""



            ###############################
            # メニューを選択してください  #
            #                             #
            # 1:新規登録                  #
            # 2:更新                      #
            # 3:参照                      #
            # 4:削除                      #
            # 5:Keyの一覧表示             #
            # 6:Redis内データ全削除       #
            # 7:Redis内データのファイル化 #
            #                      q:終了 #
            ###############################

            """)

    Menu = input('>> ')

    if Menu == 'q':
        print('本当に終了しますか？')
        num =input(' 1.はい \n 2.いいえ \n →')
        if num == '1':
            print('プログラムを終了します。')
            Exit = input('')
            logging.info('プログラムが終了しました')

            sys.exit()

        else :
            print('メニュー画面に戻ります')
            Return = input('')
            return main()

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except:
        print('ソケットの通信が切断されています。')
        Exit = input('')
        logging.info('プログラムが終了しました')

        sys.exit()

    sock.send(Menu.encode('utf-8'))
    if Menu == '1':

        logging.info('新規登録が選ばれました。')

        print('新規登録が選ばれました')
        print('')
        print('Keyを入力してください')
        Key = input('>>')
        sock.send(Key.encode('utf-8'))
        print('Valueを入力してください')
        Value = input('>>')
        sock.send(Value.encode('utf-8'))
        print('')
        print('[Key]= %s , [Value]= %s ' % (Key, Value))
        print('')
        print('登録完了しました!')

        logging.info('[Key]= %s , [Value]= %s の登録完了' % (Key, Value))

        Return = input('')
        return main()

    elif Menu == '2':

        logging.info('更新が選ばれました')

        print('更新が選ばれました')
        print('')
        print('更新したいKeyを入力してください')
        Key = input('>>')
        sock.send(Key.encode('utf-8'))
        Refer_Value = sock.recv(bufsize)
        print('[Key]= %s の [Value]の値は%sです。' % (Key, Refer_Value.decode('utf-8')))
        print('更新しますか？')
        num = input(' 1.はい \n 2.いいえ \n →')

        if num == '1':
            Update_Value = input('Valueを入力してください:')
            sock.send(Update_Value.encode('utf-8'))
            print('')
            print('[Key]= %s , [Value]= %s ' % (Key, Update_Value))
            print('更新が完了しました')

            logging.info('更新が完了しました')

            Return = input('')
            return main()

        else :
            print('メニュー画面に戻ります')
            Return = input('')
            return main()

    elif Menu == '3':

        logging.info('参照が選ばれました')

        print('参照が選ばれました')
        print('')
        print('Keyを入力してください')
        Key = input('>>')
        print('')
        sock.send(Key.encode('utf-8'))
        Keys = sock.recv(bufsize)

        R = Keys.decode('utf-8').split("/")
        for SR in R:
            print(SR)

            logging.info('[Key]の一覧表示完了')

        if R[0]=="そのようなKeyは存在していません":
            time.sleep(1)
            return main()

        elif Key == '*' or Key.find('*') >= 1:
            print('参照したいKeyを入力してください')
            print('')
            Refer_Key = input('>>')
            sock.send(Refer_Key.encode('utf-8'))
            Value = sock.recv(bufsize)

            print('[Key]= %s の [Value]の値は%sです。' % (Refer_Key, Value.decode('utf-8')))

            logging.info('[Key]= %s の [Value]= %sの参照完了。' % (Refer_Key, Value.decode('utf-8')))

            print('')
            Return = input('')
            return main()

        else:
            print('[Key]= %s の [Value]の値は%sです。' % (Key, SR))

            #logging.info('[Key]= %s の [Value]= %sの参照失敗。' )

            print('')
            Return = input('')
            return main()

    elif Menu == '4':

        logging.info('削除が選ばれました')

        print('削除が選ばれました')
        print('')
        print('Keyを入力してください')
        Key = input('>>')
        print('')
        sock.send(Key.encode('utf-8'))
        Keys = sock.recv(bufsize)

        R = Keys.decode('utf-8').split("/")
        #print(type(R))
        #print(len(R))
        if len(R) == 1 and R[0] == '0':
            print('そのようなKeyは存在しておりません')


            logging.info('削除に中止しました')

            Return = input('')
            return main()

        for SR in R:
            print(SR)

            logging.info('[Key]の一覧表示完了')

        if Key.find('*') == 1:
            print('削除したいKeyを入力してください')
            print('')
            Del_Key = input('>>')
            print('本当に削除しますか?')
            jj = input (' 1.はい \n 2.いいえ \n →')
            if jj == '1':
                sock.send(Del_Key.encode('utf-8'))

                err = sock.recv(bufsize)

                if (err.decode('utf-8')) == '1':
                    print('[Key]= %s は削除されました' % (Del_Key))

                    logging.info('[Key]= %s は削除完了' % (Del_Key))

                    Return = input('')
                    return main()

                elif (err.decode('utf-8')) == '0':
                    print('そのようなKeyは存在しておりません')

                    logging.info('削除に失敗しました')

                    Return = input('')
                    return main()

            else:
                print('メニュー画面に戻ります')
                Return = input('')
                return main()

        else:
            print('本当に削除しますか?')
            dd = input (' 1.はい \n 2.いいえ \n →')
            if dd == '1':

                sock.send(dd.encode('utf-8'))

                err = sock.recv(bufsize)

                if (err.decode('utf-8')) == '1':
                    print('[Key]= %s は削除されました' % (Key))

                    logging.info('[Key]= %s は削除完了' % (Key))

                    Return = input('')
                    return main()

                elif (err.decode('utf-8')) == '0':
                    print('そのようなKeyは存在しておりません')

                    logging.info('削除に失敗しました')

                    Return = input('')
                    return main()

            else:
                print('メニュー画面に戻ります')
                Return = input('')
                return main()

    elif Menu == '5':
        print('[Key]一覧表示します')

        logging.info('[Key]一覧表示')


        Keys = sock.recv(bufsize)
        r = Keys.decode('utf-8')
        if r==' ':
            print('Keyが一つも存在していません')
        else:
            R = Keys.decode('utf-8').split("/")
            for SR in R:
                print(SR)

            logging.info('[Key]の一覧表示完了')




        Return = input('')
        return main()

    elif Menu == '6':
        print('本当に全削除しますか？')
        num = input(' 1.はい \n 2.いいえ \n →')
        if num == '1':
            print('完了しました')
            sock.send(num.encode('utf-8'))

            logging.info('Redisデータ全削除完了')

            Return = input('')
            return main()

        else:
            sock.send(num.encode('utf-8'))
            print('メニュー画面に戻ります')
            Return = input('')
            return main()

    elif Menu == '7':
        print('[Key],[Value]をファイル化します')
        print('')
        print('[Key],[Value]のファイル化完了しました')

        logging.info('Redisデータのファイル化完了')

        Return = input('')
        return main()

    elif Menu == 'q':
        print('本当に終了しますか？')
        num =input(' 1.はい \n 2.いいえ \n →')
        if num == '1':
            print('プログラムを終了します。')
            Exit = input('')

            logging.info('プログラムが終了しました')

            sys.exit()
        else :
            print('メニュー画面に戻ります')
            Return = input('')
            return main()

    else:
        print('選択肢の中から選んでください。')
        Return = input('')
        return main()

if __name__ == '__main__':
    main()
