import datetime
import tkinter.messagebox
import requests
import sys
import time


# ==========================
# file: stock_monitor.py
# version: 1.0.0
# author: lirong
# email : aisun#gmail.com
# ==========================

class StockMonitor:
    stock_url = "http://hq.sinajs.cn/list="
    stock_lists = {
        'sh601106': {'name': '中国一重', 'min': 3.02, 'max': 3.5},
        'sh600020': {'name': '中原高速', 'min': 4.80, 'max': 5.0},
        'sz002177': {'name': '御银股份', 'min': 5.01, 'max': 5.5},
        'sz300315': {'name': '掌趣科技', 'min': 3.70, 'max': 4.2}
    }

    def __init__(self):
        tkinter.Tk().withdraw()

    def alert_message(self, message, type='info'):
        if message != '':
            if type == 'warring':
                title = "提示"
                tkinter.messagebox.showwarning(title, message)
            elif type == 'error':
                title = "警告"
                tkinter.messagebox.showerror(title, message)
            else:
                title = "提示"
                tkinter.messagebox.showinfo(title, message)

    def httpGet(self, url):
        if url != '':
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                return ""

    def run(self):
        ids = []
        for id in self.stock_lists:
            ids.append(id)

        url = self.stock_url + ','.join(ids)

        res = self.httpGet(url)
        if res == '':
            return "接口数据返回错误"
            sys.exit()
        else:
            stock_datas = res.rstrip('\n').split('\n')

            string_message = ""
            for stock_data in stock_datas:
                temp_stock_code = stock_data[11:19]  # 截取股票代码
                temp_stock_lists = stock_data[21:-2]  # 截取股票数据
                single_stock_datas = temp_stock_lists.split(',')
                min_price = self.stock_lists[temp_stock_code]['min']
                max_price = self.stock_lists[temp_stock_code]['max']
                if float(single_stock_datas[3]) < min_price:
                    string_message += "[低]名称:" + single_stock_datas[0] + ",当前价格:" + str(
                        single_stock_datas[3][0:4]) + ",设低价:" + str(min_price) + "\n"

                if float(single_stock_datas[3]) > max_price:
                    string_message += "[高]名称:" + single_stock_datas[0] + ",当前价格:" + str(
                        single_stock_datas[3][0:4]) + ",设高价:" + str(max_price) + "\n"

            if string_message != "":
                self.alert_message(string_message)


if __name__ == "__main__":
    stockMonitor = StockMonitor()

    pre_date = datetime.datetime.now().date()
    start_time = str(pre_date) + " 09:30:00"
    end_time = str(pre_date) + " 15:00:00"

    start_time_stamp = time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
    end_time_stamp = time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
    current_timestamp = time.time()

    count = 0
    while (current_timestamp > start_time_stamp) and (current_timestamp < end_time_stamp):
    # while count < 10:
        stockMonitor.run()
        time.sleep(3)
        print("当前时间:" + str(datetime.datetime.now()) + " 请求次数:" + str(count))
        count += 1
    else:
        print("当前时间:" + str(datetime.datetime.now()) + " 未在交易时间")
