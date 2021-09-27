import time
from socket import *
from threading import Thread


class TcpServer(object):
    """Tcp服务器"""

    def __init__(self):
        """初始化对象"""
        self.clients = {}
        self.time = time.strftime("%Y-%m-%d %H:%M", time.gmtime())
        self.code_mode = "utf-8"  # 收发数据编码/解码格式
        self.server_socket = socket(AF_INET, SOCK_STREAM)  # 创建socket
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)  # 设置端口复用
        self.server_socket.bind(("127.0.0.1", 9090))  # 绑定IP和Port
        self.server_socket.listen(5)  # 设置为被动socket

    def run(self):
        """运行"""
        while True:
            client_socket, client_addr = self.server_socket.accept()  # 等待客户端连接
            tr = Thread(target=self.__recv_data, args=(client_socket, client_addr))  # 创建线程为客户端服务
            tr.start()  # 开启线程

    def __recv_data(self, client_socket, client_addr):
        """收发数据"""
        while True:
            if client_socket not in [i[0] for i in self.clients.keys()]:
                try:
                    name = client_socket.recv(1024).decode(self.code_mode)
                except ConnectionResetError:
                    print(f"[WinError 10054] 远程主机{client_addr}强迫关闭了一个现有的连接。")
                    break
                enter_msg = self.time + "\n" + name + "进入聊天室...\n"
                self.__file_write(enter_msg, client_addr)
                self.clients[(client_socket, client_addr)] = name
                client_socket.send(f"欢迎你：{name}\n".encode(self.code_mode))
                continue

            try:
                message = client_socket.recv(1024).decode('utf-8')
            except ConnectionResetError:
                print(f"[WinError 10054] 远程主机{client_addr}强迫关闭了一个现有的连接。")
                self.clients.pop((client_socket, client_addr))
                break

            if '--EXIT' in message:
                leave_msg = f"{self.time}\n{self.clients[(client_socket, client_addr)]} 离开了聊天室..."
                self.clients.pop((client_socket, client_addr))
                self.__file_write(leave_msg, client_addr)

            # 用户输入"--USER_LIST"请求聊天室内在线用户列表
            elif '--USER_LIST' in message:
                for user in self.clients:
                    list_msg = f" ip: {str(user[1])} \tname: {self.clients[user]} \n".encode(self.code_mode)
                    client_socket.send(list_msg)

            elif message == "":
                print(f"{client_addr}连接已断开")
                break

            else:
                if self.time == time.strftime("%Y-%m-%d %H:%M", time.gmtime()):
                    msg = message
                else:
                    self.time = time.strftime("%Y-%m-%d %H:%M", time.gmtime())
                    msg = self.time + '\n' + message

                # 发送消息并记录
                self.__file_write(msg, client_addr)
        client_socket.close()

    def __file_write(self, msg, client_addr):
        print(msg)
        # file = open('chat_history.txt', 'a', encoding=self.code_mode)
        # file.write(f"ip: {str(client_addr)}\ttime: {msg}\n")
        # file.close()
        for address in self.clients:
            address[0].send(msg.encode(self.code_mode))


def main():
    my_server = TcpServer()
    my_server.run()


if __name__ == "__main__":
    main()
