# coding=utf-8
from stockmodel.MysqlModel import *


class Score_Rank():
    def get_user_rank(self):
        value = 8
        sql = "select user_name,user_money from user_info order by user_money desc limit %s"
        user_rank_tuple = MysqlController().db_read(sql, value)
        user_rank_list = []
        for i in user_rank_tuple:
            ul = []
            for m in i:
                ul.append(str(m))
            user_rank_str = "--".join(ul)
            user_rank_list.append(user_rank_str)
        return user_rank_list
