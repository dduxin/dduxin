from client_Gui import *


HOST = '127.0.0.1'
# HOST = '172.60.20.98'
PORT = 8421
ADDR = (HOST, PORT)
BUFFERSIZE = 1024

connfd = socket()
connfd.connect(ADDR)
# 创建登录和注册窗口的对象
land = Gui(connfd)
# 调用客户端Gui类方法,创建登录窗口
land.client_landgui(land)
mainloop()
# 判断用户是否进了登录操作，如果是直接关闭了窗口则退出程序
if land.state == 0:
    connfd.send('退出'.encode())
    os._exit(0)
# 创建主界面对象
main = Gui(connfd)
# Gui类的　实例对象　调用主界面创建函数
main.client_zjm()
# 创建线程，用来发送请求
t1 = Thread(target=chuli.send, args=(main,))
t1.start()

# # 创建线程，用来接收消息-暂未使用
# t2 = Thread(target=recv)
# t2.start()
mainloop()

connfd.send('退出'.encode())
