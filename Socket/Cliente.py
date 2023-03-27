import socket
import struct

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
    sock.connect(('127.0.0.1',50000))
    
    print(" Socket: ",sock.getsockname())
    
    msg = input("Entre com uma mensagem:").encode()
    sendmsg(sock,msg)
    
    res = recvmsg(sock)
    print("Servidor Responde: ", res.decode())
    
    sock.close()
    
    return 0

if __name__ == '__main__':
	main()