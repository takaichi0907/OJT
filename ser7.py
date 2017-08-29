import socket
import redis
import sys

import logging
LOG_FILENAME = 'SV.log'
logF = '%(asctime)s- %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=LOG_FILENAME, format=logF, level=logging.DEBUG)
logging.info('プログラムが起動しました')

r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)



def main():
    host = 'localhost'
    port = 4649
    backlog = 10
    bufsize = 4096
    select_num = 10

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    readfds = set([sock])

    try:
        sock.bind((host, port))
        sock.listen(backlog)
        print('Waiting for connections...')

        logging.info('接続中...')

        while True:
            conn, address = sock.accept()

            select_num = conn.recv(bufsize)

            if (select_num.decode('utf-8')) == '1':

                logging.info('新規登録が選ばれました')

                print('新規登録が選ばれました')
                Key = conn.recv(bufsize)
                print(Key.decode('utf-8'))
                Value = conn.recv(bufsize)
                print(Value.decode('utf-8'))
                r.set(Key, Value)
                logging.info('[Key]= %s , [Value]= %s の登録完了' % (Key, Value))



            elif (select_num.decode('utf-8')) == '2':
                logging.info('参照が選ばれました')
                print('参照が選ばれました')
                Key = conn.recv(bufsize)
                aa = Key.decode('utf-8')

                Keys = r.keys(Key)
                print(type(Key))
                for RKey in Keys:
                    qqq = str(RKey.decode('utf-8')) + "/"
                    byqqq = bytes(qqq, 'utf-8')
                    conn.send(byqqq)

                if aa.find('*') == 1:

                    Key2 = conn.recv(bufsize)

                    try:
                        refer_value = r.get(Key2)
                        print(refer_value.decode('utf-8'))
                        conn.send(refer_value)

                        logging.info('[Key]= %s の [Value]= %sの参照完了。' % (Key, refer_value.decode('utf-8')))

                    except:
                        print('Keyが存在していません')
                        err = '存在していない'
                        conn.send(err.encode('utf-8'))

                        logging.info('参照に失敗しました')

                else:
                    try:
                        refer_value = r.get(Key)
                        print(refer_value.decode('utf-8'))
                        conn.send(refer_value)

                        logging.info('[Key]= %s の [Value]= %sの参照完了。' % (Key, refer_value.decode('utf-8')))



                    except:
                        print('Keyが存在していません')
                        err = '存在していない'
                        conn.send(err.encode('utf-8'))
                        logging.info('参照に失敗しました')


            elif (select_num.decode('utf-8')) == '3':

                     logging.info('削除が選ばれました')

                     print('削除が選ばれました')

                     Key = conn.recv(bufsize)
                     print(Key.decode('utf-8'))
                     aa = Key.decode('utf-8')


                     Keys = r.keys(Key)
                     for RKey in Keys:
                         qqq = str(RKey.decode('utf-8')) + "/"
                         byqqq = bytes(qqq, 'utf-8')
                         conn.send(byqqq)


                     if aa.find('*') == 1:
                         Key2 = conn.recv(bufsize)
                         del_num = r.delete(Key2)
                         print(del_num)

                         if del_num == 1:
                             num = '1'
                             conn.send(num.encode('utf-8'))

                             logging.info('[Key]= %s は削除完了' % (Key2))

                         elif del_num == 0:
                             num = '0'
                             conn.send(num.encode('utf-8'))

                             logging.info('削除に失敗しました')

                     else:
                         del_num = r.delete(Key)
                         print(del_num)
                         if del_num == 1:
                             num = '1'
                             conn.send(num.encode('utf-8'))

                             logging.info('[Key]= %s は削除完了' % (Key))

                         elif del_num == 0:
                             num = '0'
                             conn.send(num.encode('utf-8'))

                             logging.info('削除に失敗しました')



            elif (select_num.decode('utf-8')) == '4':
                     print('プログラムの終了')

                     logging.info('プログラムが終了しました')

            elif (select_num.decode('utf-8')) == '5':
                     print('サーバーの終了')

                     logging.info('サーバーが終了しました')

                     sys.exit()

            elif (select_num.decode('utf-8')) == '6':
                     print('Redis内データの全削除が選ばれました')
                     num = conn.recv(bufsize)
                     print(num)
                     num2 = num.decode('utf-8')
                     if num2 == '1':
                         r.flushall()

                         logging.info('Redis内データ全削除完了')

                         print('Redis内のデータ全削除完了')

                     else:
                         print('メニュー画面に戻ります')

            elif (select_num.decode('utf-8')) == '7':
                print('[key]の一覧表示します')
                Keys = r.keys('*')
                for RKey in Keys:
                    qqq = str(RKey.decode('utf-8')) + "/"
                    byqqq = bytes(qqq, 'utf-8')
                    conn.send(byqqq)

                    logging.info('[Key]の一覧表示完了')


            elif (select_num.decode('utf-8')) == '8':
                    print('更新が選ばれました')
                    Key = conn.recv(bufsize)
                    print(Key.decode('utf-8'))

                    try:
                        refer_value = r.get(Key)
                        print(refer_value.decode('utf-8'))
                        conn.send(refer_value)

                    except:
                        print('Keyが存在していません')
                        err = '存在していない'
                        conn.send(err.encode('utf-8'))

                    print('更新')


                    Update_Value = conn.recv(bufsize)
                    print(Update_Value.decode('utf-8'))
                    r.set(Key, Update_Value)
                    print('更新完了')

                    logging.info('更新完了')

            elif (select_num.decode('utf-8')) == '9':
                    print('ファイル化が選ばれました')
                    res_keys = r.keys()                     # KEYS
                    if res_keys:
                        res_mget = r.mget(res_keys)         # MGET
                        f = open('write.txt', 'w')
                        f.write('[')
                        for key, val in zip(res_keys, res_mget):
                            print(key, val)

                            f.write('  \n{"Key":"%s" ,  "Value":"%s"}, ' % (key.decode('utf-8'), val.decode('utf-8')))
                        f.write('\n]')

                        f.close()






    finally:
        for sock in readfds:
            sock.close()
    return

if __name__ == '__main__':
   main()
