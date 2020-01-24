# coding=utf-8
"""
股票交易模块
"""
import easygui as g


class Stock_Trade():

    def show_plate_stock_info(self, sc, stock_plate):
        """
        根据选择的板块展示股票基本信息
        :param sc: 套接字
        :param stock_plate:板块信息
        :return: 相应的板块股票信息
        """
        msg = "ssi" + "$" + stock_plate
        sc.send(msg.encode())
        data = sc.recv(1024 * 1024 * 10).decode()
        if not data:
            return False
        stock_list = data.split("/")
        stock_choose_str = g.choicebox(msg='《%s板块的》股票信息' % stock_plate, title='股票交易', choices=stock_list)
        if not stock_choose_str:
            return "fall"
        stock_choose_id = stock_choose_str.split("--")[0]
        return stock_choose_id

    def show_select_stock_detail(self, sc, stock_id):
        """
        根据传入的股票id,获取相应股票的价格等信息
        :param stock_id:股票id
        :return:操作选择与现价股票id,str类型
        """
        signal = "sssd" + "$" + stock_id
        sc.send(signal.encode())
        data = sc.recv(1024 * 1024).decode()
        if data == "fall":
            return "fall", "fall", "fall"
        msg_list = data.split("$")
        if len(msg_list) == 0:
            return "fall", "fall", "fall"
        msg = "日期:" + msg_list[5] + "--" + "名称:" + msg_list[0] + "--" + "开盘价" + msg_list[1] + "--" \
              + "现价" + msg_list[2] + "--" + "最高价" + msg_list[3] + "--" + "最低价" + msg_list[3]
        choose_opt = g.buttonbox(msg=msg, title='股票详细信息', choices=["买入", "卖出", "日线"])
        return choose_opt, msg_list[2], stock_id

    def show_plate(self, sc):
        """
        展示所属板块信息
        :return: 返回点击选择的板块信息
        """
        signal = "sp"
        sc.send(signal.encode())
        data = sc.recv(1024).decode()
        sp_list = data.split("/")
        sp_sel = g.choicebox(msg='请选择想了解的板块', title='股票板块信息', choices=sp_list)
        if not sp_sel:
            return False
        sp_name = sp_sel.split("--")[0]
        return sp_name

    def show_plt(self, sc):
        """
        展示股票折线图
        :return:
        """
        x = range(1, 8, 1)
        # y = self.show_stock_detail(sc, (1, 2))
        # plt.plot(x, y)
        # plt.show()

    def do_stock_buy(self, sc, user_id, now_price, st_id):
        """
        玩家客户购买股票
        :param user_id:玩家id
        :param st_id:股票id
        :return:
        """
        msg = "请输入购买数量"
        while True:
            signal = "buystock" + "$" + user_id
            sc.send(signal.encode())
            back_msg = sc.recv(1024).decode().split("$")
            user_money = back_msg[1]
            if back_msg[0] == "ok":
                title = "股票购买"
                fieldNames = ["当前账户余额", "购买价格", "购买数量"]
                fieldValues = g.multenterbox(msg, title, fieldNames, values=[user_money, now_price])
                if not fieldValues:
                    break
                if len(fieldValues[2]) != 0:
                    total_money = int(fieldValues[2]) * int(fieldValues[1])
                    buy_stock_amount = fieldValues[2]
                    stock_amount = self.show_stock_amount(sc, st_id)
                    if (total_money > int(user_money)) or (stock_amount < int(buy_stock_amount)):
                        msg = "余额不足或股票数量不足"
                        continue
                    else:
                        res_st = self.do_buy_update(sc, st_id, buy_stock_amount, user_id, total_money, now_price)
                        if res_st == "ok":
                            res_succ = self.show_buy_succ()
                            if res_succ:
                                return "ok"
                            else:
                                break
                        else:
                            msg = "购买失败"
                            continue
                else:
                    msg = "输入有误请重新输入"
                    continue

    def do_buy_update(self, sc, st_id, st_buy_amount, user_id, total_money, now_price):
        signal = "dbu" + "$" + str(st_id) + "$" + str(st_buy_amount) + "$" + str(user_id) + "$" + str(
            total_money) + "$" + now_price
        sc.send(signal.encode())
        msg = sc.recv(1024).decode()
        return msg

    def show_stock_amount(self, sc, st_id):
        signal = "show_sa" + "$" + st_id
        sc.send(signal.encode())
        stock_amount = int(sc.recv(1024).decode())
        return stock_amount

    def do_stock_sell(self, sc, user_id, st_id):
        signal = "getusj" + "$" + user_id + "$" + st_id
        sc.send(signal.encode())
        back_date = sc.recv(1024).decode().split("$")
        if back_date[0] == "ne":
            return self.show_sell_fall()
        else:
            msg = "请输入卖出数量"
            while True:
                st_cou = back_date[0]
                now_price = back_date[1]
                title = "卖出股票"
                fieldNames = ["持有股票数量", "卖出价格", "卖出数量"]
                fieldValues = g.multenterbox(msg, title, fieldNames, values=[st_cou, now_price])
                if not fieldValues:
                    continue
                if (not fieldValues[2]) or (int(fieldValues[2]) > int(st_cou)):
                    msg = "输入数量错误"
                    continue
                else:
                    sig = "dosellup" + "$" + user_id + "$" + st_id + "$" + \
                          fieldValues[1] + "$" + fieldValues[2]
                    sc.send(sig.encode())
                    data = sc.recv(1024).decode()
                    if data == "ok":
                        res_succ = self.show_sell_succ()
                        if res_succ:
                            return "ok"
                        else:
                            break
                    else:
                        msg = "卖出失败"
                        continue

    def show_buy_succ(self):
        res = g.msgbox(msg="购买成功！", title="AID1911股票系统", ok_button="确定")
        return res

    def show_sell_fall(self):
        res = g.msgbox(msg="你没有持有该支股票！", title="AID1911股票系统", ok_button="确定")
        return res

    def show_sell_succ(self):
        res = g.msgbox(msg="卖出成功！", title="AID1911股票系统", ok_button="确定")
        return res
