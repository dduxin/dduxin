import os
import time
from socket import *


class Hand:

    @classmethod
    # 处理用户登录函数
    def lan(self, r, data):
        with open('usr', 'r') as f:
            while True:
                a = f.readline()
                if not a:
                    break
                b = a.split(',')
                c = data.split(',')
                if b[0] == c[1] and b[1] == c[2]:
                    r.send('登录成功'.encode())
                    return
                elif b[0] == c[1] and b[1] != c[2]:
                    r.send('用户名或密码错误'.encode())
                    return
            r.send('用户名不存在,请注册后登录'.encode())

    @classmethod
    # 处理用户注册函数
    def sign(self, r, data):
        with open('usr', 'r') as fr:
            while True:
                a = fr.readline()
                if not a:
                    break
                # 从文件读取到　的　用户名
                b = a.split(',')
                # 切割data得到用户名
                d = data.split(',')[1]
                # 如果用户名已经存在，return
                if b[0] == d:
                    # print('发送之前')
                    r.send('用户名已被占用'.encode())
                    # print('发送之后')
                    return
        # 用户名不存在，则打开usr文件，进行写入
        with open('usr', 'a') as f:
            print('打开user，执行注册')
            c = data.split(',')
            f.write(c[1] + ',' + c[2] + ',' + '100M\n')
            os.mkdir('./user/local-' + c[1])

            r.send('注册成功'.encode())

    @classmethod
    # 处理用户获取文件夹列表函数
    def view(self, r, data, user):
        lst = os.listdir('./user/local-' + user[r])  # 个人文件夹路径
        lstall = os.listdir('./share/')  # 共享文件夹路径
        # 计算个人文件夹中所有文件的大小
        size = 0
        for i in lst:
            path = './user/local-' + user[r] + '/' + i
            if os.path.isfile(path):
                s = os.path.getsize(path)
                size += s
        resize = round((100 - (size / 1024 / 1024)), 2)
        # 显示共享文件夹
        if data.split(',')[1] == '0':
            # 共享文件夹为空
            # 空，可用空间，用户名
            if not lstall:
                r.send(('空' + ',' + str(resize) + ',' + user[r]).encode())
            # 文件列表，可用空间，用户名
            else:
                r.send((','.join(lstall) + ',' +
                        str(resize) + ',' + user[r]).encode())
        # 显示个人文件夹
        elif data.split(',')[1] == '1':
            # 个人文件夹为空
            # 空，可用空间，用户名
            if not lst:
                r.send(('空' + ',' + str(resize) + ',' + user[r]).encode())
            # 文件列表，可用空间，用户名
            else:
                r.send((','.join(lst) + ',' +
                        str(resize) + ',' + user[r]).encode())

    @classmethod
    # 用户信息函数
    def userinfo(self, r, user):
        with open('./usr', 'rb') as f:
            while True:
                a = f.readline()
                if not a:
                    break
                if user[r] == a.split(',')[0]:
                    r.send((user[r] + ',' + a.split(',')[2]).encode())
                    break

    @classmethod
    # 处理删除文件请求函数
    def delete(self, r, data, user):
        filename = data.split(',')[1]
        try:
            os.remove('./user/local-' + user[r] + '/' + filename)  # 个人文件夹路径
            time.sleep(0.1)
            r.send('删除成功'.encode())
        except Exception:
            r.send('Fail'.encode())

    @classmethod
    # 处理下载请求函数
    def download(self, r, data, user):
        # 共享文件夹
        if data.split(',')[2] == '0':
            size = str(os.path.getsize(('./share/' + data.split(',')[1])))
            lstall = os.listdir('./share/')  # 共享文件夹路径
            for i in lstall:
                if i == data.split(',')[1]:
                    r.send(('可以下载' + ',' + size).encode())

        if data.split(',')[2] == '1':
            size = str(os.path.getsize(
                ('./user/local-' + str(user[r]) + '/' + data.split(',')[1])))

            lst = os.listdir('./user/local-' + user[r])  # 个人文件夹路径
            for i in lst:
                if i == data.split(',')[1]:
                    r.send(('可以下载' + ',' + size).encode())
                    # print('download发送成功')

        # # 个人文件夹
        # # '下载' + ',' + value + ',' + str(var.get())).encode()
        # if data.split(',')[2] == '1':
        #     lst = os.listdir('./user/local-' + user[r])  # 个人文件夹路径
        #     for i in lst:
        #         if i == data.split(',')[1]:
        #             r.send('可以下载'.encode())

    @classmethod
    # 处理上传请求函数
    def upload(self, r, data, user):
        # 共享文件夹
        if data.split(',')[2] == '0':
            lstall = os.listdir('./share/')  # 共享文件夹路径
            for i in lstall:
                if i == data.split(',')[1]:
                    r.send('所要上传的文件名重复，请更改后重试'.encode())
                    return
            r.send('可以上传'.encode())

        # 个人文件夹
        if data.split(',')[2] == '1':
            lstall = os.listdir('./user/local-' + user[r])

            # 计算个人文件夹中所有文件的大小
            size = 0
            for i in lstall:
                path = './user/local-' + user[r] + '/' + i
                if os.path.isfile(path):
                    s = os.path.getsize(path)
                    size += s
            if size / 1024 / 1024 >= 100:
                r.send('可用空间不足，请充值扩容'.encode())
                return
            for i in lstall:
                if i == data.split(',')[1]:
                    r.send('所要上传的文件名重复，请更改后重试'.encode())
                    return
            r.send('可以上传'.encode())

    @classmethod
    # 实现下载函数
    def down(self, r, data):
        if data.split(',')[3] == '0':
            with open(('./share/' + data.split(',')[1]), 'rb') as f:
                while True:
                    a = f.read(1024)
                    if not a:
                        break
                    r.send(a)
                time.sleep(0.1)
            r.send(b'*@!@#!!!$*')
            os._exit(0)
        elif data.split(',')[3] == '1':
            with open(('./user/local-' + data.split(',')[2] +
                       '/' + data.split(',')[1]), 'rb') as f:
                while True:
                    a = f.read(1024)
                    if not a:
                        break
                    r.send(a)
                time.sleep(0.1)
            r.send(b'*@!@#!!!$*')
            os._exit(0)

    @classmethod
    # 实现上传函数
    def up(self, data):
        HOST = '127.0.0.1'
        # HOST = '172.60.20.98'
        PORT = 8422
        ADDR = (HOST, PORT)
        connfd = socket()
        connfd.connect(ADDR)
        if data.split(',')[3] == '0':
            with open(('./share/' + data.split(',')[1]), 'wb') as f:
                while True:
                    file = connfd.recv(1024)
                    if file == b'@!!#@!#$%':
                        break
                    f.write(file)
            connfd.close()
            os._exit(0)
        elif data.split(',')[3] == '1':
            with open(('./user/local-' + data.split(',')[2] +
                       '/' + data.split(',')[1]), 'wb') as f:
                while True:
                    file = connfd.recv(1024)
                    if file == b'@!!#@!#$%':
                        break
                    f.write(file)
            connfd.close()
            os._exit(0)
