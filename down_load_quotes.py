import baostock as bs
import pandas as pd


#  http://baostock.com/baostock/index.php/A%E8%82%A1K%E7%BA%BF%E6%95%B0%E6%8D%AE

def down_quotes(symbol, start_date, end_date, frequency):
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    #### 获取历史K线数据 ####

    rs = bs.query_history_k_data_plus(symbol, "date,time,open,close",
                                      start_date=start_date, end_date=end_date,
                                      frequency=frequency, adjustflag="3")  # frequency="d"取日k线，adjustflag="3"默认不复权

    print('query_history_k_data_plus respond error_code:' + rs.error_code)
    print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())

    result = pd.DataFrame(data_list, columns=rs.fields)
    #### 结果集输出到csv文件 ####
    result.to_csv("history_" + symbol + "FROM" + start_date + "TO" + end_date + "_data.csv", encoding="gbk",
                  index=False)
    print(result)

    #### 登出系统 ####
    bs.logout()


# down_quotes("sh.601668", '2019-11-26', '2020-08-22', '5')
down_quotes("sh.601668", '2020-03-18', '2020-08-22', '5')
