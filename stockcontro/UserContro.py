# coding=utf-8
from stockmodel.MysqlModel import MysqlController


class User_Controller():
    def servers_do_register(self, user):
        """
        根据传入的用户对象,判断用户是否存在，如存在就返回存在，如果不存在就插入数据库
        :param user: 用户对象
        :return: 一个字符串
        """
        value = user.user_id
        sql1 = "select user_id from user_info where user_id=%s"
        if MysqlController().db_read(sql1, value):
            return "exsit"
        else:
            values = (user.user_id, user.user_name, user.user_password, user.user_sex,
                      user.user_phonenumber, user.user_email, user.user_money, user.user_level)
            sql2 = "insert into user_info values (%s,%s,%s,%s,%s,%s,%s,%s)"
            result = MysqlController().db_write(sql2, values)
            if result:
                return "ok"
            else:
                return "no"

    def servers_do_login(self, user):
        """
        根据传入用户对象的账号密码判断是否匹配。
        :param user: 用户对象
        :return: 字符串和用户的权限
        """
        values = user.user_id
        sql = "select user_password,user_level from user_info where user_id=%s"
        user_tuple = MysqlController().db_read(sql, values)
        if not user_tuple:
            return "notexsit"
        if user.user_password == user_tuple[0][0]:
            return "ok" + "$" + str(user_tuple[0][1])
        else:
            return "wrong"

    def servers_get_user_money(self, user):
        values = int(user.user_id)
        sql = "select user_money from user_info where user_id=%s"
        user_money_tuple = MysqlController().db_read(sql, values)
        if not user_money_tuple:
            return 0
        else:
            return str(user_money_tuple[0][0])

    def get_user_info(self, user):
        values = user.user_id
        sql = "select m.uun,si.stock_name,m.asu,si.stock_id from stock_info as si inner join " \
              "(select u.user_name as uun,a.stock_id as asi,a.su as asu,a.av as aav from " \
              "user_info as u inner join (select user_id,stock_id,sum(ub_amount) as su," \
              "avg(buy_price) as av from user_buy where user_id=%s and operate=1 group by stock_id) as a " \
              "on u.user_id=a.user_id) as m on si.stock_id=m.asi;"
        gui_tuple = MysqlController().db_read(sql, values)
        if not gui_tuple:
            gui_tuple = ((0, 0, 0, 0))
        sql2 = "select stock_id,sum(ub_amount) from user_buy where user_id=%s and operate=0 group by stock_id"
        res_tuple = MysqlController().db_read(sql2, values)
        if not res_tuple:
            res_tuple = ((0, 0))
        sql1 = "select user_name from user_info where user_id=%s"
        un = MysqlController().db_read(sql1, values)
        gui_list = []

        for i in gui_tuple:
            list_1 = []
            for m in i:
                list_1.append(m)
            gui_list.append(list_1)

        for l in gui_list:
            for n in res_tuple:
                if l[3] == n[0]:
                    l[2] -= n[1]

        for h in range(len(gui_list) - 1, -1, -1):
            if gui_list[h][2] == 0:
                del gui_list[h]

        if gui_list[0][2] == 0:
            return ["用户:" + un[0][0] + "--" + "当前未持有股票", ""]
        back_list = []
        for i in gui_list:
            info_str = "用户:" + i[0] + "--" + "股票ID:" + i[3] + "--" + "股票:" + i[1] + "--" \
                       + "持有量:" + str(i[2])
            back_list.append(info_str)
        return back_list

    def judge_user_stock(self, user, stock):
        ui = user.user_id
        sql = "select sum(ub_amount) from user_buy where user_id=%s and operate=1 group by stock_id"
        res = MysqlController().db_read(sql, ui)
        if not res:
            res = ((0, 0), (0, 0))
        sql1 = "select sum(ub_amount) from user_buy where user_id=%s and operate=0 group by stock_id"
        res1 = MysqlController().db_read(sql1, ui)
        if not res1:
            res1 = ((0, 0), (0, 0))
        if (res[0][0] - res1[0][0]) > 0:
            now_price = self.get_now_price(stock)
            st_cou = self.get_sell_info(user, stock)
            return str(st_cou) + "$" + str(now_price)
        else:
            return "ne"

    def get_sell_info(self, user, stock):
        ui = user.user_id
        si = stock.stock_id
        values = (ui, si)
        sql = "select sum(ub_amount) from user_buy where user_id=%s and operate=1 and stock_id=%s group by stock_id"
        res = MysqlController().db_read(sql, values)
        sql1 = "select sum(ub_amount) from user_buy where user_id=%s and operate=0 and stock_id=%s group by stock_id"
        res1 = MysqlController().db_read(sql1, values)
        if not res:
            res = ((0, 0))
        if not res1:
            res1 = ((0, 0), (0, 0))
        a = int(res[0][0]) - res1[0][0]
        return a

    def get_now_price(self, stock):
        values = stock.stock_id
        sql = "select now_price from stock_price where stock_id=%s order by sp_date desc limit 1"
        data = MysqlController().db_read(sql, values)
        return data[0][0]
