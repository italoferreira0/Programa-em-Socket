import socket
import struct
from collections import Counter

def count(a):
    cont = str(Counter(a))
    return cont.split('{')[1].split('}')[0]

def recvall(sock, length):
    data = b""
    while len(data) < length:
        more = sock.recv(length - len(data))
        
        if not more:
            raise EOFError("Falha ao receber os dados esperados.")
        data += more
    return data

def recvmsg(sock):
    tam = struct.unpack("!i",recvall(sock,4))[0]
    return recvall(sock,tam)

def sendmsg(sock,msg):
    sock.sendall(struct.pack("!i",len(msg)))
    sock.sendall(msg)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1',50000))
    sock.listen(1)
    
    print("Ouvindo em", sock.getsockname())
    
    while True:
        sc, sockname = sock.accept()
        
        msg = recvmsg(sc)   	 
        mensagem = msg.decode()
        print(mensagem)
        if mensagem[:5] == 'UPPER':
            sendmsg(sc,mensagem[5:].upper().encode())
        elif mensagem[:5] == 'LOWER':
            sendmsg(sc,mensagem[5:].lower().encode())
        elif mensagem[:3] == 'LEN':
            sendmsg(sc,str(len(mensagem[4:])).encode())
        elif mensagem[:5] == 'COUNT':
            sendmsg(sc,str(count(mensagem[6:])).encode())
        elif mensagem[:5] == 'WORDS':
            lista = len((mensagem[6:]).split(' '))
            print(lista)
            sendmsg(sc,str(lista).encode())

        sendmsg(sc,msg.decode().encode())
        
        sc.close()
   	 
    return 0

if __name__ == '__main__':
	main()