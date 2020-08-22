import csv

class Position(object):
    def __init__(self, symbol, price, quantity):
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.cost = quantity * price
        self.sell_times = 0
        self.buy_times = 0

    def nlv(self):
        return round(self.quantity * self.price, 3)

    def get_cost(self):
        return self.cost

    def desc(self):
        return self.symbol + "\t[持仓：" + str(self.quantity) + "\t当前股价：" + str(self.price) + "\tnlv：" + str(
            self.nlv()) + "\t成本：" + str(self.get_cost()) + "\t收益：" + str(self.nlv() - self.get_cost()) + "]"

    def buy(self, current_price, quantity, time_str):
        self.price = current_price
        self.quantity += quantity
        self.cost += current_price * quantity
        self.buy_times += 1
        print("持仓变动+"+ str(self.buy_times) + "\ttime: " + time_str + " \tbuy:" + str(quantity) + "\tat:" + str(current_price) + "\t" + self
              .desc())
        return True

    def sell(self, current_price, quantity, time_str):
        if self.quantity < quantity:
            print("not enough")
            return False
        self.price = current_price
        self.quantity -= quantity
        self.cost -= current_price * quantity
        self.sell_times -= 1
        print("持仓变动"+ str(self.sell_times) + "\ttime: " + time_str + " \tsell:" + str(quantity) + "\tat:" + str(current_price) + "\t" + self
              .desc())
        return True


class Grid(object):
    def __init__(self, symbol, base_price, min_price, max_price, base_quantity, single_quantity, grid_value):
        self.base_price = base_price
        self.min_price = min_price
        self.max_price = max_price
        self.base_quantity = base_quantity
        self.single_quantity = single_quantity
        self.grid_value = grid_value
        self.symbol = symbol
        self.position = Position(symbol, self.base_price, self.base_quantity)
        self.next_up_price = self.next_up(base_price)
        self.next_down_price = self.next_down(base_price)

    def get_next_up(self):
        return self.next_up(self.base_price)

    def get_next_down(self):
        return self.next_down(self.base_price)

    def next_down(self, base_price):
        return round(base_price - self.grid_value, 3)

    def next_up(self, base_price):
        return round(base_price + self.grid_value, 3)

    def stress_test(self):
        print("压力测试开始：如果股价一直下跌")
        price = self.base_price
        while True:
            price = self.next_down(price)
            if price < self.min_price:
                break
            self.position.buy(price, self.single_quantity, "x")

        ## 重置
        self.position = Position(self.symbol, self.base_price, self.base_quantity)
        print("压力测试结束\n")

    def revenue_test(self):
        print("收益测试开始：如果股价一直上涨")
        price = self.base_price
        while True:
            price = self.next_up(price)

            if self.position.sell(price, self.single_quantity,'x'):
                continue
            else:
                break
                ## 重置
        self.position = Position(self.symbol, self.base_price, self.base_quantity)
        print("收益测试结束\n")

    def on_price_change(self, cur_price, time_str):
        t = time_str[:12]
        while True:
            up_price = self.get_next_up()
            down_price = self.get_next_down()
            if cur_price >= up_price and up_price <= self.max_price:
                if self.position.sell(up_price, self.single_quantity, t):
                    self.base_price = up_price
                else:
                    break
            elif cur_price <= down_price and down_price >= self.min_price:
                self.position.buy(down_price, self.single_quantity, t)
                self.base_price = down_price
            else:
                break

grid = Grid("中国建筑", 5.22, 4, 6, 5500, 900, 0.1)
grid.stress_test()

with open("/Users/huangyuming/github/grid_trade/history_sh.601668FROM2020-03-18TO2020-08-22_data.csv", 'r') as csvFile:
    # 读取csv文件,返回的是迭代类型
    reader = csv.reader(csvFile)
    flag = True
    for item in reader:
        if flag:
            flag = False
            continue
        # print(item)
        grid.on_price_change(float(item[2]), item[1])
        grid.on_price_change(float(item[3]), item[1])

csvFile.close()
