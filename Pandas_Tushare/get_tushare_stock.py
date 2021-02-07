import tushare as ts
import pandas as pd
import datetime as dt
from sqlalchemy import create_engine
from config_mysql import ConfSql
import time
import threading, queue,sys


class GetStock():

    def __init__(self):
        ts.set_token("30d023679cd931ae49506267e9a80fdba42641655150c8fa656ae416")
        self.data = []
        self.pro = ts.pro_api()

    # 获取当前所有正常上市交易的股票代码
    def get_stock_code(self):

        self.data = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code')
        self.set_stock_code()

    # 保存data至CSV
    def set_stock_code(self):
        self.data.to_csv('data/Stock_codes.csv')
        # print(dt.datetime.now().strftime('%Y%m%d'))


   # 获取每一只股票的历史数据
    def code_frame(self):
        codes = pd.read_csv('data/Stock_codes.csv')
        for row in codes.itertuples():
            self.flags = getattr(row, 'ts_code')
            self.trans = self.flags.replace('.','_')
            # print(getattr(row,'name'),getattr(row,'ts_code'))
            self.df = self.pro.daily(ts_code=self.flags, start_date='20180701', end_date=dt.datetime.now().strftime('%Y%m%d'))
            # df.to_csv('data/transactiondata/'+(getattr(row,"ts_code"))+'.csv')
            cs = ConfSql()
            cs.create_table(self.trans)
            self.put_mysql()
    def put_mysql(self):
        engine = create_engine(r'mysql+pymysql://root:mySQL.root.4415@localhost:3306/Stock?charset=utf8')
        self.df.to_sql(self.trans, engine, index=False, if_exists='replace')
        print(self.trans,'写入SQL完成')

todo_queue = queue.Queue()
done_queue = queue.Queue()

class MoreThread(threading.Thread):

    def __init__(self, func, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func

    def run(self):
        while True:
            try:
                task = todo_queue.get(False)
                if task:
                    self.func()
                    done_queue.put(1)
            except queue.Empty:
                print('todo_queue=None')
                break
        return

workers = []
gs = GetStock()
# mt = MoreThread(func=gs.code_frame())
for i in range(50):
    todo_queue.put(i)
# for i in range(5):
#         mt = MoreThread(func=gs.code_frame())
#         workers.append(mt+i)
#
# for i in range(5):
#     workers[i].start()
#
# for i in range(5):
#     workers[i].join()

while todo_queue.empty() == False:
    mt = MoreThread(func=gs.code_frame())
    workers.append(mt + i)
    print('当前线程数：',i)
    mt+i.start()
for i in workers:
    i.join()
total_num = done_queue.qsize()
print("TOTAL_HANDLE_TASK: %d" % total_num)
sys.exit(0)