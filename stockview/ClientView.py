# coding=utf-8
"""
系统客户端主页面
"""
from stockview.UserView import *
from stockview.StockView import *
from stockview.AdminManagerView import *
from socket import *


class Client_View():
    def __init__(self):
        self.sc = socket()
        self.sc.connect(("127.0.0.1", 8088))

    def main(self):
        while True:
            # 先选择是登录还是注册信息，如果为０就进入注册界面，如果为１就跳过
            sel = User_View().user_choice()
            if sel == 1:
                pass
            elif sel == 0:
                result = User_View().register(self.sc)
                if not result:
                    continue
            else:
                break
            # 进行玩家用户登录
            user_level, user_id = User_View().do_login(self.sc)
            # 如果用户权限为１就是管理员,如果为０就是普通玩家用户。
            if user_level == "1":
                # 管理员跳转到玩家用户管理界面
                while True:
                    ms = Admin_Manager().admin_manager_select(self.sc)
                    if not ms:
                        break
                    else:
                        Admin_Manager().do_user_opetare(self.sc, ms)
            elif user_level == "0":
                while True:
                    ui = user_id
                    sel = User_View().show_user_info(self.sc, ui)
                    if not sel:
                        break
                    else:
                        # 普通用户就跳转到玩家用户分数排名界面
                        ur = User_View().user_rank(self.sc)
                        if not ur:
                            continue
                        else:
                            # 点击确定后就跳转到股票板块展示界面,玩家用户选择想要交易的板块
                            sp_sel = Stock_Trade().show_plate(self.sc)
                            if not sp_sel:
                                continue
                            else:
                                # 根据玩家选择的板块信息，展示出相应板块对应的股票信息。
                                sps = sp_sel
                                choo_stock_id = Stock_Trade().show_plate_stock_info(self.sc, sps)
                                if choo_stock_id != "fall":
                                    # 根据玩家选择的股票信息，展示被选股票的价格等信息，让玩家买卖。
                                    ssd_res, now_price, st_id = Stock_Trade().show_select_stock_detail(self.sc,
                                                                                                       choo_stock_id)
                                    if st_id == "fall":
                                        continue
                                    if ssd_res == "买入":
                                        # 购买股票
                                        Stock_Trade().do_stock_buy(self.sc, user_id, now_price, st_id)
                                        continue
                                    elif ssd_res == "卖出":
                                        # 卖出股票
                                        Stock_Trade().do_stock_sell(self.sc, user_id, st_id)
                                        continue
                                    else:
                                        pass  ###
                                else:
                                    continue
            else:
                continue


if __name__ == '__main__':
    Client_View().main()
