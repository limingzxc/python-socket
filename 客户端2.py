from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


class TcpClient(object):
    """Tcp客户端"""

    def __init__(self, ip_, port_):
        """初始化对象"""
        self.code_mode = "utf-8"  # 收发数据编码/解码格式
        self.IP = ip_
        self.Port = port_
        self.my_socket = socket(AF_INET, SOCK_STREAM)  # 创建socket

    def run(self):
        """启动"""
        try:
            self.my_socket.connect((self.IP, self.Port))  # 连接服务器
            tr = Thread(target=self.recv_data)  # 创建线程收数据
            ts = Thread(target=self.send_data)  # 创建线程发数据

            tr.start()  # 开启线程
            ts.start()
        except ConnectionRefusedError:
            print("[WinError 10061] 由于目标计算机积极拒绝，无法连接。")

    def recv_data(self):
        """收数据"""
        self.my_socket.send(name.encode(self.code_mode))
        while True:
            try:
                data = self.my_socket.recv(1024).decode(self.code_mode)
                if data == "":
                    print("连接服务器失败")
                    break
            except ConnectionAbortedError:
                print("[WinError 10054] 远程主机强迫关闭了一个现有的连接。")
                break
            except ConnectionResetError:
                print("[WinError 10054] 远程主机强迫关闭了一个现有的连接。")
                break
            print(data)
        self.my_socket.close()

    def send_data(self):
        """发数据"""
        while True:
            string = input("")
            message = name + ": " + string + "\n"
            try:
                self.my_socket.send(message.encode(self.code_mode))
            except ConnectionResetError:
                print("[WinError 10054] 远程主机强迫关闭了一个现有的连接。")
                break
            if "--EXIT" in message:
                self.my_socket.close()
                break


if __name__ == "__main__":
    print('____WELCOME____\n' + 'EXIT -> exits\nUSER_LIST -> get users')
    # ip = input("please input your ip:")
    # port = input("please input your port:")
    # name = input('please input your name:')
    ip = "127.0.0.1"
    port = "9090"
    name = "a"
    my_socket = TcpClient(ip, int(port))
    my_socket.run()
