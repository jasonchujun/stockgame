# coding=utf-8
import easygui as g


class User_View():

    def user_choice(self):
        """
        初始界面，玩家用户选择登录或者注册。
        :return: ０或者１
        """
        msg = "欢迎来到AID1911股票交易系统"
        title = 'AID1911股票交易系统首页'
        user_choice = g.ccbox(msg, title, choices=("登录账号", "注册账号"))
        return user_choice

    def register(self, sc):
        """
        玩家注册界面
        :param sc:传入的客户端套接字
        :return: 无返回值
        """
        msg = "请输入注册信息(其中带*号的项为必填项)"
        while True:
            title = "用户注册"
            fieldNames = ["*账号", "*真实姓名", "*密码", "*性别", "*手机号码", "*Email"]
            fieldValues = g.multenterbox(msg, title, fieldNames)
            while True:
                if not fieldValues:
                    break
                errmsg = ""
                for i in range(len(fieldNames)):
                    option = fieldNames[i].strip()
                    if fieldValues[i].strip() == "" and option[0] == "*":
                        errmsg += ("【%s】为必填项   " % fieldNames[i])
                if errmsg == "":
                    break
                fieldValues = g.multenterbox(errmsg, title, fieldNames, fieldValues)
            if not fieldValues:
                break
            data = "regi" + "$" + "$".join(fieldValues)
            sc.send(data.encode())
            message = sc.recv(1024)
            if message == "exsit".encode():
                msg = "用户已存在"
                continue
            elif message == "ok".encode():
                break
            else:
                msg = "注册失败，重新注册"
                continue

    def do_login(self, sc):
        """
        玩家登录界面
        :param sc:传入的客户端套接字
        :return: 玩家用户的权限和用户id
        """
        msg = "请输入账号和密码"
        while True:
            title = "用户登录"
            user_info = g.multpasswordbox(msg, title, ["账号", "密码"])
            if not user_info:
                break
            user_info_str = "".join(user_info)
            if len(user_info_str) == 0:
                continue
            else:
                data = "login" + "$" + "$".join(user_info)
                sc.send(data.encode())
                mes = sc.recv(1024).decode()
                mes_list = mes.split("$")
                if mes_list[0] == "ok":
                    return mes_list[1], user_info[0]
                elif mes_list[0] == "wrong":
                    msg = "账号密码不符"
                    continue
                else:
                    msg = "账号不存在"
                    continue

    def user_rank(self, sc):
        """
        展示用户总金额排名信息
        :param sc: 传入的客户端套接字
        :return: 返回用户选择，有值为继续或者　空为退出
        """
        signal = "urank"
        sc.send(signal.encode())
        back_msg = sc.recv(1024).decode()
        user_rank_msg = back_msg.split("/")
        sel = g.choicebox(msg='玩家账户余额排名', title='玩家排名', choices=user_rank_msg)
        return sel

    def do_user_update(self, sc, user_id, total_money):
        signal = "duu" + "$" + user_id + "$" + total_money
        sc.send(signal.encode())
        msg = sc.recv(1024).decode()
        return msg

    def show_user_info(self, sc, user_id):
        signal = "getui" + "$" + str(user_id)
        sc.send(signal.encode())
        data = sc.recv(1024).decode()
        ui_list = data.split("/")
        sel = g.choicebox(msg='玩家基本信息', title='玩家信息', choices=ui_list)
        return sel
