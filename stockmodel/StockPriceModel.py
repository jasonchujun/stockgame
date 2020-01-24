# coding=utf-8
class Stock_Price_Model():
    def __init__(self, sp_id=None, s_price=None, e_price=None, max_price=None, min_price=None, sp_date=None,
                 stock_id=None, now_price=None):
        self.sp_id = sp_id
        self.s_price = s_price
        self.e_price = e_price
        self.max_price = max_price
        self.min_price = min_price
        self.sp_date = sp_date
        self.stock_id = stock_id
        self.now_price = now_price