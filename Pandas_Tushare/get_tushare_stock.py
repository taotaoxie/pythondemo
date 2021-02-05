import tushare as ts
import pandas as pd

class GetStock():
    data = []
    def __init__(self):
        ts.set_token("30d023679cd931ae49506267e9a80fdba42641655150c8fa656ae416")


    def get_stock_data(self):
        pro = ts.pro_api()
        # 获取当前所有正常上市交易的股票列表
        self.data = pro.stock_basic()
        self.set_stock_data()
        print(self.data)

    def set_stock_data(self):
        self.data.to_csv('data/Stock_data.csv')

gt = GetStock()
gt.get_stock_data()