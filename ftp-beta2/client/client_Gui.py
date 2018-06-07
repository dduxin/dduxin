from client_chuli import *
import math


class Gui:

    def __init__(self, connfd):
        self.connfd = connfd
        self.state = 0

    # 创建注册窗口(在登录窗口的基础上创建)
    def client_signgui(self, t, v):
        # 重置登录窗口提示语
        v.set('')
        # 创建注册窗口
        top2 = Toplevel(t)
        top2.title("注册")
        top2.geometry("400x250+200+20")
        Label(top2, text="用户名:").place(x=50, y=40)
        Label(top2, text="密码:").place(x=50, y=80)
        Label(top2, text="确认密码:").place(x=50, y=120)
        # 创建注册窗口提示语
        var = StringVar()
        Label(top2, textvariable=var).place(x=120, y=190)
        # 用户名输入框
        ns = Variable()
        ns.set("请输入用户名")
        entrynames = Entry(top2, textvariable=ns)
        entrynames.place(x=120, y=40)
        # 用户密码输入框
        pwds = Variable()
        entrypwds = Entry(top2, textvariable=pwds, show="*")
        entrypwds.place(x=120, y=80)
        # 用户密码确认输入框
        pwds1 = Variable()
        entrypwds1 = Entry(top2, textvariable=pwds1, show="*")
        entrypwds1.place(x=120, y=120)
        # 提交注册按钮
        b_sign = Button(
            top2, text='注册', command=lambda: chuli.usrsign
            (var, ns, pwds, pwds1, top2, self.connfd))
        b_sign.place(x=130, y=150)
        top2.mainloop()

    # 创建登录窗口
    def client_landgui(self, obj):
        top = Tk()
        top.title("登录")
        top.geometry("400x300+200+20")
        #
        bm = PhotoImage(file='/home/tarena/桌面/bata/timg.gif',)
        # /home/tarena/桌面/测试

        label2 = Label(top, image=bm, height=145)
        label2.bm = bm
        label2.pack()

        Label(top, text="用户名:").place(x=50, y=150)
        Label(top, text="密码:").place(x=50, y=190)
        # 创建窗口提示语
        var = StringVar()
        Label(top, textvariable=var).place(x=120, y=270)
        # 用户名输入框
        n = Variable()
        n.set("请输入用户名")
        entryname = Entry(top, textvariable=n)
        entryname.place(x=120, y=150)
        # 用户密码输入框
        pwd = Variable()
        entrypwd = Entry(top, textvariable=pwd, show="*")
        entrypwd.place(x=120, y=190)
        # 登录按钮
        b_login = Button(
            top, text='登录', command=lambda:
            chuli.land_client(n, var, pwd, top, self.connfd, obj))
        b_login.place(x=130, y=230)
        # 注册按钮
        b_sign = Button(
            top, text='注册', command=lambda:
            Gui.client_signgui(self, top, var))
        b_sign.place(x=230, y=230)

    def client_zjm(self):
        # 创建用户界面
        self.top1 = Tk()
        self.top1.title("FTP文件管理系统")
        self.top1.geometry("600x400+200+20")
        # 创建文件夹选择容器
        self.fr1 = LabelFrame(self.top1, width=150, height=100, text='文件夹')
        self.fr1.grid(row=0, column=0, padx=5)
        # 创建文件列表等容器
        self.fr2 = LabelFrame(self.top1, width=250, height=390, text='文件列表')
        self.fr2.grid(row=0, column=1, padx=5, rowspan=24)
        # 创建用户信息容器
        self.fr3 = LabelFrame(self.top1, width=150, height=100, text='用户信息')
        self.fr3.grid(row=1, column=0)
        # 创建下载信息容器
        self.fr4 = LabelFrame(self.top1, width=150, height=190, text='上传下载信息')
        self.fr4.grid(row=2, column=0)
        # 创建文件列表
        self.filelist2 = Listbox(self.fr2)
        self.filelist2.place(x=0, y=0, width=230, height=334)
        # 创建文件列表的滚动条
        self.sb2 = Scrollbar(self.fr2)
        self.sb2.place(x=230, y=0, height=333)

        # 文件列表 关联 滚动条
        self.filelist2.config(yscrollcommand=self.sb2.set)

        # ？ 滚动条 关联 文件列表的增减
        # self.sb2.config(command=self.filelist2.yview)



    def sendgui(self, view, download, upload, delete):
        self.var = IntVar()  # 创建了一个各项文件夹的变量
        self.var.set(0)  # 初始设置为显示共享文件夹
        # L = ['共享文件夹', '个人文件夹']
        # for i in range(2):
        #     rb1 = Radiobutton(self.fr1, text=L[i], font=(10),
        #                       variable=self.var, value=i,
        #                       command=lambda: view(self.var, self.t, self.t1))
        #     rb1.place(x=0, y=i * 35)
        # value　设置此控件代表的值
        # variable 设置此控件关联的变量
        rb1 = Radiobutton(self.fr1, text='共享文件夹', font=(10),
                          variable=self.var, value=0,
                          command=lambda: view(self.var, self.t, self.t1))
        rb1.place(x=0, y=0)
        rb2 = Radiobutton(self.fr1, text='个人文件夹', font=(10),
                          variable=self.var, value=1,
                          command=lambda: view(self.var, self.t, self.t1))
        rb2.place(x=0, y=35)
        # 创建用户信息容器中的Label
        Label(self.fr3, text='用户名:', font=10).place(x=0, y=5)
        Label(self.fr3, text='剩余空间:', font=10).place(x=0, y=35)
        # t用户名 t1用户可用空间
        self.t = StringVar()
        self.t1 = StringVar()
        Label(self.fr3, textvariable=self.t, font=10).place(x=80, y=5)
        Label(self.fr3, textvariable=self.t1, font=10).place(x=80, y=35)
        # 创建下载信息容器中的Label
        Label(self.fr4, text='文件名:').place(x=0, y=0)
        Label(self.fr4, text='进度:').place(x=0, y=20)
        # d1　　文件名
        # dj1　进度条
        self.d1 = StringVar()
        self.dj1 = StringVar()
        Label(self.fr4, textvariable=self.d1).place(x=40, y=0)
        Label(self.fr4, textvariable=self.dj1).place(x=31, y=20)
        Label(self.fr4, text='文件名:').place(x=0, y=55)
        Label(self.fr4, text='进度:').place(x=0, y=75)
        self.d2 = StringVar()
        self.dj2 = StringVar()
        Label(self.fr4, textvariable=self.d2).place(x=40, y=55)
        Label(self.fr4, textvariable=self.dj2).place(x=31, y=75)
        Label(self.fr4, text='文件名:').place(x=0, y=105)
        Label(self.fr4, text='进度:').place(x=0, y=125)
        self.d3 = StringVar()
        self.dj3 = StringVar()
        Label(self.fr4, textvariable=self.d3).place(x=40, y=105)
        Label(self.fr4, textvariable=self.dj3).place(x=31, y=125)

        # 创建文件列表容器中的按钮
        # 参数为 文件夹
        Button(self.fr2, text="下载", command=lambda: download(
            self.var)).place(x=190, y=335)
        # 参数为 文件夹 用户名 可以空间
        Button(self.fr2, text="刷新", command=lambda: view(
            self.var, self.t, self.t1)).place(x=139, y=335)
        # 参数为 文件夹
        Button(self.fr2, text="上传", command=lambda: upload(
            self.var)).place(x=0, y=335)
        # 参数为 文件夹
        Button(self.fr2, text="删除", command=lambda: delete(
            self.var)).place(x=88, y=335)

    # 显示进度条第一步　显示文件名
    # self为Gui类 文件名　共享内存的值
    def jindu(self, filename, value):
        # 文件名　列表
        self.Lb = [self.d1, self.d2, self.d3]
        # 进度条　列表
        self.Lbj = [self.dj1, self.dj2, self.dj3]
        # 主界面的　文件名位置　设置文件名
        self.Lb[value - 1].set(filename)

        self.ci = 0  # 根据文件大小统计需要循环多少次，进而计算出每循环多少次为100分之1
        self.bfb = 1  # 用来计数显示百分百
        self.bfbh = 1  # 用来计数显示进度条
        return

    # 显示进度条第二步　显示进度条
    # self为Gui类　文件大小　共享内存的值
    def jinduview(self, filesize, value):
        self.ci += 1
        # 传输次数
        # math.ceil(filesize / 1024)
        # # 多少个 >
        # self.bfbh = c / n * 100
        # self.Lbj[value - 1].set('[%s]%d%%' % (('>' * self.bfbh), self.bfbh))

        # 如果ci　等于文件大小的　1%　
        if self.ci == int(filesize / 1024 / 100):
            # 跟新
            self.Lbj[value - 1].set('[%s]%d%%' % (('>' * self.bfbh), self.bfb))
            self.ci = 0
            self.bfb += 1
            if self.bfb % 10 == 0:
                self.bfbh += 1
                return

    # 弹窗询问
    def messageboxask(self, title, msg):
        ask = tkinter.messagebox.askyesno(title=title, message=msg)
        return ask

    # 弹窗提醒
    def messageboxinfo(self, title, msg):
        tkinter.messagebox.showinfo(title=title, message=msg)

    # 更改文件名
    def rename(self):
        top3 = Toplevel(self.top1)
        top3.title("文件重命名")
        top3.geometry("320x50+400+200")

        def re():
            self.newname = nname.get()
            top3.destroy()
            return

        Label(top3, text="输入新文件名:", font=8).place(x=10, y=10)
        nname = Variable()
        Entry(top3, textvariable=nname).place(x=115, y=10)
        Button(top3, text="确定", command=re).place(x=265, y=10)

        top3.mainloop()
