import socket
import time

# 创建UDP套接字
svrsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 绑定
svrsocket.bind(('127.0.0.1', 8080))
# 聊天室内用户，用字典存放，{(ip:port):用户名}
users = {}


def send_record(msg):
    '''
    接收一个字符串
    打印并传递给write2file和broadcast
    通过该方法可在服务器和用户上看见用户进入/离开聊天室以及用户聊天信息
    同时将上述信息写入文件(通过write2file)
    '''
    print(msg)
    write2file(msg)
    broadcast(msg)


def write2file(string):
    '''
    接收一个字符串
    可将字符串作为单独的一行追加到文件末尾
    用于将聊天信息记录到文件中
    '''
    file = open('chat.txt', 'a', encoding="utf-8")
    file.write(string + "\n")
    file.close()


def broadcast(msg):
    '''
    在套接字中广播(给每个用户都发送msg)
    把每个用户发送的信息都发送给其他用户
    '''
    # 遍历用户字典users
    for address in users:
        svrsocket.sendto(msg.encode(), address)


while True:
    try:
        # 从UDP套接字接收到信息
        user_data, user_addr = svrsocket.recvfrom(1024)

        # 新用户加入聊天室
        if not user_addr in users:
            # 该用户进入聊天室的msg
            enter_msg = time.asctime() + "\n" + user_data.decode() + "进入聊天室..."
            # 该用户进入聊天室，发送提示并记录到文件
            send_record(enter_msg)
            # 将该用户添加到用户字典users
            users[user_addr] = user_data.decode('utf-8')
            print(users)
            # 新用户进入聊天室，无需再判断user_data
            continue

        # 用户输入"--EXIT"退出聊天
        if '--EXIT' in user_data.decode('utf-8'):
            # 用户离开聊天室的msg
            leave_msg = time.asctime() + "\n" + users[user_addr] + "离开了聊天室..."
            # 用户字典删除该用户
            users.pop(user_addr)
            # 用户退出聊天室，发送提示并记录到文件
            send_record(leave_msg)

        # 用户输入"--USERLIST"请求聊天室内在线用户列表
        elif '--USERLIST' in user_data.decode('utf-8'):
            # 遍历存放用户的字典users
            for user in users.keys():
                # list_msg = username+ip+port
                list_msg = (users[user] + ': ' + user[0] + ":" + str(user[1])).encode()
                # 单独发送给请求userlist的用户
                svrsocket.sendto(list_msg, user_addr)

        else:
            # 聊天室内用户正常聊天
            msg = time.asctime() + '\n' + user_data.decode('utf-8')
            # 发送消息并记录
            send_record(msg)

    except ConnectionResetError:
        print("ConnectionResetError")
