# coding=utf-8
from stockmodel.MysqlModel import MysqlController


class Stock_Controller():

    def get_stock_info(self, stock):
        """
        获取股票信息
        :param stock: 列表,列表内数据以$进行拼接.
        :return:返回股票信息列表
        """
        value = stock.stock_plate
        sql = "select stock_id,stock_name,stock_amount,stock_ipo " \
              "from stock_info where stock_plate=%s order by stock_id"
        stock_tuple = MysqlController().db_read(sql, value)
        stock_list2 = []
        for i in range(len(stock_tuple)):
            stock_list1 = []
            for n in range(len(stock_tuple[i])):
                stock_list1.append(str(stock_tuple[i][n]))
            str1 = "--".join(stock_list1)
            stock_list2.append(str1)
        return stock_list2

    def get_select_stock_price(self, stock_price):
        """
            根据传入的stock_id查询出选择的股票价格信息
        :param stock:stock对象
        :return:
        """
        value = stock_price.stock_id
        sql = "select si.stock_name,sp.s_price,sp.now_price,sp.max_price,sp.min_price,sp.sp_date " \
              "from stock_info as si inner join stock_price as sp on si.stock_id=sp.stock_id " \
              "where sp.stock_id=%s order by sp.sp_date desc limit 1;"
        sp_tuple = MysqlController().db_read(sql, value)
        if not sp_tuple:
            return "fall"
        stock_plate_list = []
        for n in range(len(sp_tuple[0])):
            stock_plate_list.append(str(sp_tuple[0][n]))
        str1 = "$".join(stock_plate_list)
        return str1

    def get_stock_plate(self):
        """
        获取股票数量前10的板块信息
        :return: 返回一个板块信息列表
        """
        sql = "select stock_plate,count(stock_id) from stock_info group by stock_plate " \
              "having count(stock_id)>10 order by count(stock_id) desc limit %s"
        st_pla_tuple = MysqlController().db_read(sql, 10)
        stock_plate_list2 = []
        for i in range(len(st_pla_tuple)):
            stock_plate_list1 = []
            for n in range(len(st_pla_tuple[i])):
                stock_plate_list1.append(str(st_pla_tuple[i][n]))
            str1 = "--".join(stock_plate_list1)
            stock_plate_list2.append(str1)
        return stock_plate_list2

    def get_stock_amount(self, stock):
        """
        查询出股票原有可卖数量
        :param stock:股票对象
        :return:剩余可卖数量int类型
        """
        values = stock.stock_id
        sql = "select stock_amount from stock_info where stock_id=%s"
        stock_amount_tuple = MysqlController().db_read(sql, values)
        if len(stock_amount_tuple) == 0:
            return 0
        else:
            return stock_amount_tuple[0][0]
