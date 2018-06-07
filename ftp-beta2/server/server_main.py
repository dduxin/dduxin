from socket import *
import select
from server_handle import *  # 导入登录操自定义模块
import os
from multiprocessing import Process
import signal

s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 8421))
# s.bind(('172.60.20.98', 8421))
s.listen(5)

# 创建IO多路复用模型，用来接收客户端的初步操作请求
rlist = [s]
wlist = []
xlist = []
user = {}  # 用于储存登录中用户的信息


while True:
    try:
        rs, ws, es = select.select(rlist, wlist, xlist)
        for r in rs:
            if r is s:
                c, addr = r.accept()
                print("连接到", addr)
                rlist.append(c)
                xlist.append(c)
            else:
                data = r.recv(1024).decode()
                if data.split(',')[0] == '登录':
                    Hand.lan(r, data)
                    # 创建字典 键为客户套接字，值为用户名
                    # 客户端套接字c:用户名
                    user[r] = data.split(',')[1]
                elif data.split(',')[0] == '注册':
                    Hand.sign(r, data)
                elif data.split(',')[0] == '文件夹':
                    Hand.view(r, data, user)
                elif data.split(',')[0] == '用户信息':
                    Hand.userinfo(r, user)
                elif data.split(',')[0] == '下载':
                    Hand.download(r, data, user)
                elif data.split(',')[0] == '开始下载':
                    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
                    p = Process(target=Hand.down, args=(r, data))
                    p.start()
                    # p.join()
                elif data.split(',')[0] == '上传':
                    Hand.upload(r, data, user)
                elif data.split(',')[0] == '开始上传':
                    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
                    p = Process(target=Hand.up, args=(data,))
                    p.start()
                    # p.join()
                elif data.split(',')[0] == '删除':
                    Hand.delete(r, data, user)
                elif data == '互传':
                    pass
                elif data == '退出':
                    del user[r]
                    rlist.remove(r)
                    xlist.remove(r)
                    r.close()

        for w in ws:
            pass
        for e in es:
            if e is s:
                s.close()
                sys.exit(0)
            else:
                e.close()
                rlist.remove(e)
                xlist.remove(e)
    except KeyboardInterrupt:
        s.close()
        os._exit(0)
    except Exception:
        continue
