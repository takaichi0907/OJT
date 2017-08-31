import socket
import redis
import sys
import logging
LOG_FILENAME = 'SV.log'
logF = '%(asctime)s- %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=LOG_FILENAME, format=logF, level=logging.DEBUG)

argPort = sys.argv

#logging.info('プログラムが起動しました')

r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

def main():
    host = 'localhost'
    if len(argPort) == 1:
        port = 4649
    else :
        port = int(argPort[1])
    backlog = 10
    bufsize = 4096
    Menu = 10

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    readfds = set([sock])

    try:
        sock.bind((host, port))
        sock.listen(backlog)
        print('Waiting for connections...')
        logging.info('プログラムが起動しました')
        logging.info('接続中...')

        while True:
            conn, address = sock.accept()
            Menu = conn.recv(bufsize)



            if (Menu.decode('utf-8')) == '1':

                logging.info('新規登録が選ばれました')

                print('新規登録が選ばれました')
                Key = conn.recv(bufsize)
                print(Key.decode('utf-8'))
                Value = conn.recv(bufsize)
                print(Value.decode('utf-8'))
                r.set(Key, Value)

                logging.info('[Key]= %s , [Value]= %s の登録完了' % (Key.decode('utf-8'), Value.decode('utf-8')))

            elif (Menu.decode('utf-8')) == '2':
                print('更新が選ばれました')
                Key = conn.recv(bufsize)
                print(Key.decode('utf-8'))

                Refer_Value = r.get(Key)
                print(Refer_Value)

                if Refer_Value == None:
                    print('Keyが存在していません')
                    err = '存在していない'
                    conn.send(err.encode('utf-8'))

                    logging.info('更新中止')

                else:
                    conn.send(Refer_Value)
                    print('更新')
                    Update_Value = conn.recv(bufsize)
                    if Update_Value.decode('utf-8') == '1':

                        logging.info('更新中止')

                    else:
                        print(Update_Value.decode('utf-8'))
                        r.set(Key, Update_Value)
                        print('更新完了')

                        logging.info('更新完了')



            elif (Menu.decode('utf-8')) == '3':

                logging.info('参照が選ばれました')

                print('参照が選ばれました')
                Key = conn.recv(bufsize)
                aa = Key.decode('utf-8')

                qqq = '' #初期値なし

                if aa.find('*') == 1:
                    Keys = r.keys(Key)
                    print(type(Key))
                    for RKey in Keys:
                        qqq = qqq + str(RKey.decode('utf-8')) + "/"
                    byqqq = bytes(qqq, 'utf-8')
                    conn.send(byqqq)
                    Refer_Key = conn.recv(bufsize)

                    try:
                        Refer_Value = r.get(Refer_Key)
                        print(Refer_Value.decode('utf-8'))
                        conn.send(Refer_Value)

                        logging.info('[Key]= %s の [Value]= %sの参照完了。' % (Key.decode('utf-8'), Refer_Value.decode('utf-8')))

                    except:
                        print('Keyが存在していません')
                        err = '存在していない'
                        conn.send(err.encode('utf-8'))

                        logging.info('参照に失敗しました')

                else:
                    try:
                        Refer_Value = r.get(Key)
                        print(Refer_Value.decode('utf-8'))
                        conn.send(Refer_Value)

                        logging.info('[Key]= %s の [Value]= %sの参照完了。' % (Key.decode('utf-8'), Refer_Value.decode('utf-8')))

                    except:
                        print('Keyが存在していません')
                        err = '存在していない'
                        conn.send(err.encode('utf-8'))

                        logging.info('参照に失敗しました')

            elif (Menu.decode('utf-8')) == '4':

                logging.info('削除が選ばれました')

                print('削除が選ばれました')
                Key = conn.recv(bufsize)
                print(Key.decode('utf-8'))
                aa = Key.decode('utf-8')
                Keys = r.keys(Key)
                print(Keys)
                print(type(Keys))
                if Keys == []:
                    pp = '78'
                    print('そのようなKeyはありません')
                    conn.send(pp.encode('utf-8'))

                    logging.info('削除中止')

                else:
                    for RKey in Keys:
                        qqq = str(RKey.decode('utf-8')) + "/"
                        byqqq = bytes(qqq, 'utf-8')
                        conn.send(byqqq)


                    if aa.find('*') == 1:
                        Del_Key = conn.recv(bufsize)
                        if (Del_Key.decode('utf-8')) == '8':
                            logging.info('削除中止')

                        else:
                            Del_Num = r.delete(Del_Key)
                            print(Del_Num)

                            if Del_Num == 1:
                                num = '1'
                                conn.send(num.encode('utf-8'))

                                logging.info('[Key]= %s は削除完了' % (Del_Key.decode('utf-8')))

                            elif Del_Num == 0:
                                num = '0'
                                conn.send(num.encode('utf-8'))

                                logging.info('削除に失敗しました')

                    else:
                        yy = conn.recv(bufsize)
                        zz = yy.decode('utf-8')
                        if zz == '1':
                            Del_Num = r.delete(Key)
                            print(Del_Num)

                            if Del_Num == 1:
                                num = '1'
                                conn.send(num.encode('utf-8'))

                                logging.info('[Key]= %s は削除完了' % (Key.decode('utf-8')))

                            elif Del_Num == 0:
                                num = '0'
                                conn.send(num.encode('utf-8'))

                                logging.info('削除を中止しました')

                        else:

                            logging.info('削除を中止しました')

            elif (Menu.decode('utf-8')) == '5':
                print('[key]の一覧表示します')
                Keys = r.keys('*')
                print(Keys)
                if len(Keys)==0:
                    conn.send(b' ')
                else:
                    for RKey in Keys:
                        qqq = str(RKey.decode('utf-8')) + "/"
                        byqqq = bytes(qqq, 'utf-8')
                        conn.send(byqqq)

                    logging.info('[Key]の一覧表示完了')

            elif (Menu.decode('utf-8')) == '6':
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

            elif (Menu.decode('utf-8')) == '7':
                print('ファイル化が選ばれました')
                Res_Keys = r.keys()                     # KEYS
                if Res_Keys:
                    Res_Mget = r.mget(Res_Keys)         # MGET
                    f = open('write.txt', 'w')
                    f.write('[')
                    for key, val in zip(Res_Keys, Res_Mget):
                        print(key, val)


                        f.write('  \n{"%s":"%s"}, ' % (key.decode('utf-8'), val.decode('utf-8')))
                    f.write('\n]\n')
                    f.close()

                logging.info('Redis内データのファイル化完了')






    finally:
        for sock in readfds:
            sock.close()
    return

if __name__ == '__main__':

    main()
