class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def print_score(self):
        print('%s: %s' % (self.name, self.score))


class Position(object):
    def __init__(self, symbol, price, quantity):
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.cost = quantity * price

    def nlv(self):
        return self.quantity * self.price

    def get_cost(self):
        return self.cost

    def desc(self):
        return self.symbol + "\t持仓：" + str(self.quantity) + "\t当前股价：" + str(self.price) + "\tnlv：" + str(
            self.nlv()) + "\t成本：" + str(self.get_cost()) + "\t收益：" + str(self.nlv() - self.get_cost())

    def buy(self, current_price, quantity):
        self.price = current_price
        self.quantity += quantity
        self.cost += current_price * quantity
        print("持仓变动  buy:" + str(quantity) + " at:" + str(current_price) + "\t" + self
              .desc())
        return True

    def sell(self, current_price, quantity):
        if self.quantity < quantity:
            print("not enough")
            return False
        self.price = current_price
        self.quantity -= quantity
        self.cost -= current_price * quantity
        print("持仓变动 sell:" + str(quantity) + " at:" + str(current_price) + "\t" + self
              .desc())
        return True

class Grid(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score


symbol = "sh.600036"
from_date = "2020-06-20"
to_date = "2020-08-10"

base_price = 5
base_qua = 10000

position = Position("sh.600036", 37, 1000)
position.sell(40, 1000)
position.buy(37,1000)
position.sell(40, 1000)
