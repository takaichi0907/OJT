import socket
import redis
import sys
import logging
LOG_FILENAME = 'SV.log'
logF = '%(asctime)s- %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=LOG_FILENAME, format=logF, level=logging.DEBUG)
logging.info('wake_program')
 r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
 
 
 
def main():
    host = 'localhost'
    port = 4649
    backlog = 10
    bufsize = 4096
    select_num = 100
    func_num = 10 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    readfds = set([sock])
 
    try:
        sock.bind((host, port))
        sock.listen(backlog)
        print('Waiting for connections...')
        logging.info('connecting')
  
        while True:
            conn, address = sock.accept()
  
            func_num = conn.recv(select_num)
            print(func_num.decode('utf-8'))
 
            if (func_num.decode('utf-8')) == '1':
                logging.info('select_regist')
                print('新規登録')
                msg = conn.recv(bufsize)
                print(msg.decode('utf-8'))
                msg2 = conn.recv(bufsize)
                print(msg2.decode('utf-8'))
                r.set(msg, msg2)                
                logging.info('regist_comp')
 
            elif (func_num.decode('utf-8')) == '2':
                logging.info('select_refer')
                print('参照')
                msg = conn.recv(bufsize)
                print(msg.decode('utf-8'))
 
                try:
                    refer_value = r.get(msg)
                    print(refer_value.decode('utf-8'))
                    conn.send(refer_value)
                    logging.info('refer_comp')
                except:
                    print('Keyが存在していません')
                    err = '存在していない'
                    conn.send(err.encode('utf-8'))
                    logging.info('refer_miss')
 
 
            elif (func_num.decode('utf-8')) == '3':
                logging.info('select_del')
                print('削除')
                msg = conn.recv(bufsize)
                print(msg.decode('utf-8'))
                
                del_num = r.delete(msg)
                print(del_num)
                if del_num == 1:
                    num = '1'
                    conn.send(num.encode('utf-8'))
                    logging.info('del_comp')
                    
                if del_num == 0:
                    num = '0'
                    conn.send(num.encode('utf-8'))
                    logging.info('del_miss')
 
            elif (func_num.decode('utf-8')) == '4':
                print('プログラムの終了')
 
            elif (func_num.decode('utf-8')) == '5':
                print('サーバーの終了')
                logging.info('sleep_server')
                sys.exit()
 
 
    finally:
        for sock in readfds:
        sock.close()
    return
 
 
if __name__ == '__main_'
    main()
