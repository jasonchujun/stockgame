# coding=utf-8

from stockmodel.MysqlModel import *


class Manager_Contro():
    def get_user_info(self):
        value = 0
        sql = "select user_id,user_name,user_sex,user_money,user_phonenumber from user_info where user_level=%s"
        user_info_tuple = MysqlController().db_read(sql, value)
        ui_list = []
        for item in user_info_tuple:
            ui_str = "用户ID:" + str(item[0]) + "--" + "用户名:" + str(item[1]) + "--" + "性别:" + str(item[2]) \
                     + "--" + "资金余额:" + str(item[3]) + "--" + "电话:" + str(item[4])
            ui_list.append(ui_str)
        return ui_list

    def do_user_update(self, user):
        values = (user.user_sex, user.user_email, user.user_phonenumber, user.user_id)
        sql = "update user_info set user_sex=%s,user_email=%s,user_phonenumber=%s where user_id=%s"
        res = MysqlController().db_write(sql, values)
        if res:
            return "ok"
        else:
            return "fall"
