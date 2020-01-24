# coding=utf-8
import pymysql


class MysqlController():
    def __init__(self):
        # 打开数据库连接
        self.__db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password="123456", database='stock',
                                    charset='utf8')
        self.__cursor = self.__db.cursor()

    def db_read(self, sql, values):
        self.__cursor.execute(sql, values)
        select_tuple = self.__cursor.fetchall()
        self.__db.close()
        return select_tuple

    def db_write(self, sql, values):
        try:
            self.__cursor.execute(sql, values)
            self.__db.commit()
            self.__db.close()
            return True
        except Exception:
            self.__db.rollback()
            self.__db.close()
            return False

    def do_buy_update(self, stock_surp, stock, money_surp, user, st_buy_amount, buy_price):
        v1 = (stock_surp, stock.stock_id)
        sql1 = "update stock_info set stock_amount=%s where stock_id =%s"
        v2 = (money_surp, int(user.user_id))
        sql2 = "update user_info set user_money=%s where user_id =%s"
        v3 = (int(user.user_id), stock.stock_id, st_buy_amount, buy_price)
        sql3 = "insert into user_buy (user_id,stock_id,ub_date,ub_amount,buy_price,operate) values (%s,%s,now(),%s,%s,1)"
        try:
            self.__cursor.execute(sql1, v1)
            self.__cursor.execute(sql2, v2)
            self.__cursor.execute(sql3, v3)
            self.__db.commit()
            self.__db.close()
            return True
        except Exception:
            self.__db.rollback()
            self.__db.close()
            return False

    def do_sell_update(self, stock_surp, stock, money_surp, user, sell_price, sell_amount):
        v1 = (stock_surp, stock.stock_id)
        sql1 = "update stock_info set stock_amount=%s where stock_id =%s"
        v2 = (money_surp, int(user.user_id))
        sql2 = "update user_info set user_money=%s where user_id =%s"
        v3 = (int(user.user_id), stock.stock_id, sell_amount, sell_price)
        sql3 = "insert into user_buy (user_id,stock_id,ub_date,ub_amount,buy_price,operate) values (%s,%s,now(),%s,%s,0)"
        try:
            self.__cursor.execute(sql1, v1)
            self.__cursor.execute(sql2, v2)
            self.__cursor.execute(sql3, v3)
            self.__db.commit()
            self.__db.close()
            return True
        except Exception:
            self.__db.rollback()
            self.__db.close()
            return False
