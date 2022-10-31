from strategy import Stock
import pandas as pd
import matplotlib.pyplot as plt
# Ques 1

a = Stock(start_date='2020/10/1', end_date='2022/10/30')
print(0)
benchmark_equity_curve = a.portfolio_equity_curve()
print(1)
# Ques 2

a = Stock(start_date='2020/10/1', end_date='2022/10/30')
top_10_stock = a.stock_top_n(10)
a = Stock(start_date='2020/10/1', end_date='2022/10/30', stock_list=top_10_stock)
equity_curve_top_10_stock = a.portfolio_equity_curve()
print(2)
# Ques 3

a = Stock(start_date='2020/10/1', end_date='2022/10/30', stock_list=['%5ENSEI'])
equity_curve_nifty_index = a.portfolio_equity_curve()
print(3)
# Ques 4

a = Stock(start_date='2020/10/1', end_date='2022/10/30', stock_list=['%5ENSEI'])
equity_curve_nifty_index = a.portfolio_equity_curve()
CAGR_nifty_index = a.CAGR(equity_curve_nifty_index)
Volatility_nifty_index = a.votality(equity_curve_nifty_index)
Sharpe_ratio_nifty_index = a.sharpe_ratio()
print(4)
a = Stock(start_date='2020/10/1', end_date='2022/10/30')
equity_curve_benchmark = a.portfolio_equity_curve()
CAGR_benchmark = a.CAGR(equity_curve_benchmark)
Volatility_benchmark = a.votality(equity_curve_benchmark)
Sharpe_ratio_benchmark = a.sharpe_ratio()
print(5)
a = Stock(start_date='2020/10/1', end_date='2022/10/30', stock_list=top_10_stock)
equity_curve_top_10 = a.portfolio_equity_curve()
CAGR_top_10 = a.CAGR(equity_curve_top_10)
Volatility_top_10 = a.votality(equity_curve_top_10)
Sharpe_ratio_top_10 = a.sharpe_ratio()
print(6)



