from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from tkinter import Tk, Button, Label, Entry, StringVar
from tkinter.messagebox import showerror, showwarning, showinfo


class TcpClient(object):
    """Tcp客户端"""

    def __init__(self, ip_, port_, name_):
        """初始化对象"""
        self.code_mode = "utf-8"  # 收发数据编码/解码格式
        self.IP = ip_
        self.Port = port_
        self.name = name_
        self.my_socket = socket(AF_INET, SOCK_STREAM)  # 创建socket

    def run(self):
        """启动"""
        try:
            self.my_socket.connect((self.IP, self.Port))  # 连接服务器
            self.my_socket.send(self.name.encode(self.code_mode))
        except ConnectionRefusedError:
            return 'a'
        except Exception:
            return 'b'
        else:
            return 'c'

    def send(self, message):
        self.my_socket.send(message.encode(self.code_mode))

    def recv(self):
        return self.my_socket.recv(1024).decode(self.code_mode)

    def close(self):
        self.my_socket.close()


class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("Fist Widow")
        self.window.geometry("500x400")

        self.txt_ip = Label(self.window, text="ip: ", font=("Arial Bold", 13))
        self.txt_port = Label(self.window, text="port: ", font=("Arial Bold", 13))
        self.txt_name = Label(self.window, text="name: ", font=("Arial Bold", 13))
        self.txt_ = Label(self.window, text="---------input----------", font=("Arial Bold", 13))

        self.ip_ = Entry(self.window, width=10)
        self.port_ = Entry(self.window, width=10)
        self.name_ = Entry(self.window, width=10)
        self.ip_.insert(0, "127.0.0.1")
        self.port_.insert(0, "9090")
        self.name_.insert(0, "黎明的曙光")

        self.btn = Button(self.window, text="Ping", command=self.__ping)
        self.btn_ = True

        self.word = ""
        self.msg = StringVar()
        self.txt = Label(self.window, textvariable=self.msg, font=("Arial Bold", 10))

        self.input_ = Entry(self.window, width=50)
        self.enter = Button(self.window, text="Enter", command=self.__send)

    def run(self):
        self.__top()
        self.window.mainloop()

    def __top(self):
        self.txt_ip.grid(column=0, row=0)
        self.ip_.grid(column=1, row=0)
        self.ip_.focus()
        self.txt_port.grid(column=2, row=0)
        self.port_.grid(column=3, row=0)
        self.txt_name.grid(column=4, row=0)
        self.name_.grid(column=5, row=0)
        self.btn.grid(column=6, row=0)
        self.txt_.grid(column=0, row=1, columnspan=6)
        self.input_.grid(column=0, row=2, columnspan=6)
        self.enter.grid(column=6, row=2)
        self.txt.grid(column=0, row=3, columnspan=8)

    def __ping(self):
        if self.btn_:
            ip = self.ip_.get()
            port = self.port_.get()
            name = self.name_.get()
            if not ip or not port or not name:
                showwarning('警告', '请输入内容')
            else:
                self.my_socket = TcpClient(ip, int(port), name)
                value = self.my_socket.run()
                if value == 'a':
                    showerror('错误', '连接失败')
                elif value == 'b':
                    showwarning('警告', '请检查ip和port')
                elif value == 'c':
                    showinfo('提示', '连接成功')
                    self.btn_ = False
                    self.name = name
                    self.tr = Thread(target=self.__send_data)
                    self.tr.setDaemon(True)
                    self.tr.start()
        else:
            showerror('错误', '已连接')

    def __send_data(self):
        i = 0
        while True:
            try:
                data = self.my_socket.recv()
                if data == "":
                    showerror('错误', '连接失败')
                    self.btn_ = True
                    break
            except ConnectionAbortedError:
                showerror('错误', '连接失败')
                self.btn_ = True
                break
            except ConnectionResetError:
                showerror('错误', '连接失败')
                self.btn_ = True
                break
            if len(data) > 65:
                data = data[0:62] + "...\n"
            self.word += data
            if i > 17:
                self.word = self.word[self.word.find("\n")+1:]
            self.msg.set(self.word)
            i += 1
        self.my_socket.close()

    def __send(self):
        string = self.input_.get()
        if string == "":
            showwarning('警告', '请输入文本')
        elif self.btn_:
            showwarning('警告', '未连接服务器')
        elif string == "--EXIT":
            self.my_socket.send("--EXIT")
            exit()
        else:
            self.input_.delete(0, "end")
            message = self.name + ": " + string + "\n"
            try:
                self.my_socket.send(message)
            except ConnectionResetError:
                showerror('错误', '连接失败')
                self.btn_ = True


if __name__ == "__main__":
    app = GUI()
    app.run()
