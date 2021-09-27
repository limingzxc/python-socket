import socket
import threading


def send(sock, addr):
    '''
    该函数接受一个套接字和一个元组(地址，端口)
    可通过input()获取用户输入，将信息发送给套接字
    '''
    while True:
        # 获取用户输入
        string = input()
        # 发送输入信息
        message = name + ": " + string
        sock.sendto(message.encode('utf-8'), addr)
        # 用户输入exit退出聊天
        if string == '--EXIT':
            break


def recv(sock, addr):
    '''
    该函数接受一个套接字和一个元组(地址，端口)
    可通过套接字接收服务端发过来的信息
    '''
    sock.sendto(name.encode('utf-8'), addr)
    while True:
        data = sock.recv(1024)
        print(data.decode('utf-8'))


print('____WELCOME____\n' + 'EXIT -> exits\nUSERLIST -> get users')
# 获取用户名
name = input('please input your name:')
# 建立套接字
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server = ('127.0.0.1', 8080)
# 多线程接收和发送
tr = threading.Thread(target=recv, args=(socket, server), daemon=True)
ts = threading.Thread(target=send, args=(socket, server))
tr.start()
ts.start()
ts.join()
socket.close()
