import socket, logging, threading, time

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.DEBUG,datefmt="%H:%M:%S")
HEADER=12
PORT=5050
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
FORMAT="Utf8"
DISCONNECTION="quit"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)


def client(conn,addr):
    logging.info("[NEW CONNECTION] %s connected ",str(addr))
    connected=True
    while connected:
        msg_len=conn.recv(HEADER).decode(FORMAT)
        if msg_len:
            msg_len=int(msg_len)
            msg = conn.recv(msg_len).decode(FORMAT)
            if msg==DISCONNECTION:
                connected=False
                logging.info("%s leaved.",str(addr))
            else:
                print(f"[{addr}] {msg}")
    conn.close()

def start():
    s.listen()
    logging.info(f"[LISTENING] Server is listening on {SERVER} ...")
    while 1:
        conn,addr=s.accept()
        th = threading.Thread(target=client,args=(conn,addr))
        th.start()
        time.sleep(0.000001)
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}",end='\n')


logging.info("[SERVER] Server is starting...")
start()
