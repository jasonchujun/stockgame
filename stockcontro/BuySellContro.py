from stockcontro.StockContro import *
from stockcontro.UserContro import *


class Buy_Sell_Contro():
    def do_buy_update(self, stock, st_buy_amount, user, total_money, buy_price):
        """
        更新买入股票信息
        :param stock: 股票对象
        :param st_buy_amount: 购买的数量
        :return:"ok"或者"fall"str类型
        """
        stock_amount = Stock_Controller().get_stock_amount(stock)
        user_money = User_Controller().servers_get_user_money(user)
        money_surp = int(user_money) - int(total_money)
        stock_surp = int(stock_amount) - int(st_buy_amount)
        res = MysqlController().do_buy_update(stock_surp, stock, money_surp, user, int(st_buy_amount),
                                              int(buy_price))
        if res:
            return "ok"
        else:
            return "fall"

    def do_sell_update(self, user, stock, sell_price, sell_amount):
        """
            更新卖出股票信息
        :param user:用户对象
        :param stock:股票对象
        :param sell_price:卖出价格
        :param sell_amount:卖出数量
        :return:str结果
        """
        stock_amount = Stock_Controller().get_stock_amount(stock)
        user_money = User_Controller().servers_get_user_money(user)
        money_surp = int(user_money) + (int(sell_amount) * int(sell_price))
        stock_surp = int(stock_amount) + int(sell_amount)
        res = MysqlController().do_sell_update(stock_surp, stock, money_surp, user, int(sell_price), int(sell_amount))
        if res:
            return "ok"
        else:
            return "fall"
