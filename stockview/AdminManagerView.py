# coding=utf-8
import easygui as g


class Admin_Manager():
    def admin_manager_select(self, sc):
        """
        展示出所有玩家用户信息，供管理员操作
        :return:
        """
        # 传递ams到服务器,用user类封装接受到的信息
        signal = "adms"
        sc.send(signal.encode())
        data = sc.recv(1024).decode()
        ui_info = data.split("/")
        sel = g.choicebox(msg='用户基本信息', title='用户信息', choices=ui_info)
        return sel

    def admin_manager_update(self, sc, user_id):
        """
        管理员更新玩家用户信息
        :return:
        """
        # 传递amu到服务器
        ui = user_id[-1:-2:-1]
        msg = "修改用户信息"
        while True:
            title = "用户信息修改"
            fieldNames = ["性别", "手机号码", "Email"]
            fieldValues = g.multenterbox(msg, title, fieldNames)
            if not fieldValues:
                break
            else:
                count = 0
                for item in fieldValues:
                    if item != "":
                        count += 1
                if count == 3:
                    signal = "updateu" + "$" + ui + "$" + "$".join(fieldValues)
                    sc.send(signal.encode())
                    res = sc.recv(1024).decode()
                    if not res:
                        break
                    elif res == "ok":
                        self.show_update_succ()
                        break
                    else:
                        msg = "修改失败，请重新填写"
                        continue
                else:
                    msg = "请输入完整的信息修改"
                    continue

    def do_user_opetare(self, sc, ms):
        msg_list = ms.split("--")
        user_id = msg_list[0]
        res = g.ccbox(msg=ms, title='用户管理', choices=['修改用户信息', "确定"])
        if res == 1:
            self.admin_manager_update(sc, user_id)
        else:
            return True

    def show_update_succ(self):
        res = g.msgbox(msg="修改成功！", title="AID1911股票系统", ok_button="确定")
        return res
