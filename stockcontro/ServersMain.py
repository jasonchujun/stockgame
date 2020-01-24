# coding=utf-8
"""
服务端主界面
"""
from stockmodel.UserInfoModel import *
from stockmodel.StockInfoModel import *
from multiprocessing import Process
from stockcontro.ScoreRank import *
from stockmodel.StockPriceModel import *
from stockcontro.BuySellContro import *
import time
import sys
from socket import *
import signal
from stockcontro.ManagerContro import *

ADDR = ("0.0.0.0", 8088)


class Service_Main():
    def __init__(self):
        self.ss = socket()
        self.ss.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.ss.bind(ADDR)
        self.ss.listen(5)
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    def thread_do(self, conn):
        while True:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            data = msg.split("$")
            user = User_Info_Model()
            stock = Stock_Info_Model()
            stock_price = Stock_Price_Model()
            if data[0] == "login":
                user.user_id, user.user_password = int(data[1]), data[2]
                result = User_Controller().servers_do_login(user)
                conn.send(result.encode())
            elif data[0] == "regi":
                user.user_id, user.user_name, user.user_password, user.user_sex, \
                user.user_phonenumber, user.user_email, user.user_money = int(data[1]), data[2], \
                                                                          data[3], data[4], data[5], data[6], 200000
                result = User_Controller().servers_do_register(user)
                conn.send(result.encode())
            elif data[0] == "urank":
                user_rank_list = Score_Rank().get_user_rank()
                users_rank = "/".join(user_rank_list)
                conn.send(users_rank.encode())
            elif data[0] == "sp":
                st_pl_list = Stock_Controller().get_stock_plate()
                st_pl_info = "/".join(st_pl_list)
                conn.send(st_pl_info.encode())
                time.sleep(0.1)
            elif data[0] == "ssi":
                stock.stock_plate = data[1]
                result = Stock_Controller().get_stock_info(stock)
                res_str = "/".join(result)
                conn.send(res_str.encode())
            elif data[0] == "sssd":
                stock_price.stock_id = data[1]
                sp_str = Stock_Controller().get_select_stock_price(stock_price)
                conn.send(sp_str.encode())
            elif data[0] == "buystock":
                user.user_id = int(data[1])
                user_money = User_Controller().servers_get_user_money(user)
                conn.send(("ok" + "$" + user_money).encode())
            elif data[0] == "dbu":
                stock.stock_id = data[1]
                user.user_id = int(data[3])
                st_buy_amount = int(data[2])
                total_money = int(data[4])
                buy_price = data[5]
                res = Buy_Sell_Contro().do_buy_update(stock, st_buy_amount, user, total_money, buy_price)
                conn.send(res.encode())
            elif data[0] == "show_sa":
                stock.stock_id = data[1]
                res = str(Stock_Controller().get_stock_amount(stock))
                conn.send(res.encode())
            elif data[0] == "getui":
                user.user_id = data[1]
                gui_list = User_Controller().get_user_info(user)
                gui_str = "/".join(gui_list)
                conn.send(gui_str.encode())
            elif data[0] == "getusj":
                user.user_id = data[1]
                stock.stock_id = data[2]
                res = User_Controller().judge_user_stock(user, stock)
                conn.send(res.encode())
            elif data[0] == "dosellup":
                user.user_id = data[1]
                stock.stock_id = data[2]
                sell_price = data[3]
                sell_amount = data[4]
                res = Buy_Sell_Contro().do_sell_update(user, stock, sell_price, sell_amount)
                conn.send(res.encode())
            elif data[0] == "adms":
                res = Manager_Contro().get_user_info()
                res_str = "/".join(res)
                conn.send(res_str.encode())
            elif data[0] == "updateu":
                user.user_id, user.user_sex, user.user_phonenumber, user.user_email \
                    = data[1], data[2], data[3], data[4]
                res = Manager_Contro().do_user_update(user)
                conn.send(res.encode())
            else:
                conn.close()
                self.ss.close()

    def main(self):
        while True:
            try:
                conn, addr = self.ss.accept()
                print("connect from:", addr)
            except KeyboardInterrupt:
                self.ss.close()
                sys.exit()
            except Exception:
                continue
            th = Process(target=self.thread_do, args=(conn,))
            th.start()


if __name__ == '__main__':
    Service_Main().main()
