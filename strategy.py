import pandas as pd
import numpy as np
from datetime import datetime
import traceback
from logger import logs


class Stock:
    def __init__(self, start_date, end_date, stock_list=None):

        """
        :param start_date: Enter the start date of calculation. Enter date in YYYY/MM/DD format
        :param end_date: enter the end date of stock. By default, current date is taken. Enter date in YYYY/MM/DD format
        :param stock_list: List of stock in portfolio. Default is nifty_stock_list
        """
        self.log = logs()
        self.log.write_log('Inside the class "Stocks"')
        self.log.write_log('Start date is {}'.format(start_date))
        self.log.write_log('End date is {}'.format(end_date))

        if stock_list is None:
            stock_list = ['ADANIENT', 'ADANIPORTS', 'APOLLOHOSP', 'ASIANPAINT', 'AXISBANK', 'BAJAJ-AUTO', 'BAJAJFINSV',
                          'BAJFINANCE', 'BHARTIARTL', 'BPCL', 'BRITANNIA', 'CIPLA', 'COALINDIA', 'DIVISLAB', 'DRREDDY',
                          'EICHERMOT', 'GRASIM', 'HCLTECH', 'HDFC', 'HDFCBANK', 'HDFCLIFE', 'HEROMOTOCO', 'HINDALCO',
                          'HINDUNILVR', 'ICICIBANK', 'INDUSINDBK', 'INFY', 'ITC', 'JSWSTEEL', 'KOTAKBANK', 'LT', 'M&M',
                          'MARUTI', 'NESTLEIND', 'NTPC', 'ONGC', 'POWERGRID', 'RELIANCE', 'SBILIFE', 'SBIN',
                          'SUNPHARMA',
                          'TATACONSUM', 'TATAMOTORS', 'TATASTEEL', 'TCS', 'TECHM', 'TITAN', 'ULTRACEMCO', 'UPL',
                          'WIPRO']
        self.log.write_log('Stock list is {}'.format(stock_list))

        lst = start_date.split('/')
        self.start_date = datetime(int(lst[0]), int(lst[1]), int(lst[2])).date().strftime('%s')

        lst = end_date.split('/')
        self.end_date = datetime(int(lst[0]), int(lst[1]), int(lst[2])).date().strftime('%s')

        self.stock = stock_list

        self.stock_open = pd.DataFrame()
        self.stock_close = pd.DataFrame()
        self.stock_qnt = pd.DataFrame()
        self.stock_daily_val = pd.DataFrame()
        self.stock_top_10_performance = pd.DataFrame()
        self.__stock_equity_curve = pd.DataFrame()
        self.__Daily_return_std = None
        self.__Daily_return_mean = None

    def portfolio_equity_curve(self, investment=1000000):

        """
        Calculate the 'portfolio equity curve'.

        :param investment: Invested amount. Default value is 1000000
        :return: Return the DataFrame of portfolio_equity_curve

        """
        self.log.write_log("Inside the method {}".format('portfolio_equity_curve'))
        self.log.write_log("Investment is {}".format(investment))

        try:
            for i in range(len(self.stock)):
                try:
                    link = "https://query1.finance.yahoo.com/v7/finance/download/{0}.NS?period1={1}&period2={2}&interval=1d&events=history&includeAdjustedClose=true".format(
                        self.stock[i], self.start_date, self.end_date)
                    stock_data = pd.read_csv(link)
                    self.log.write_log('link generated is'.format(link))

                except:
                    link = "https://query1.finance.yahoo.com/v7/finance/download/{0}?period1={1}&period2={2}&interval=1d&events=history&includeAdjustedClose=true".format(
                        self.stock[i], self.start_date, self.end_date)
                    stock_data = pd.read_csv(link)
                    self.log.write_log('link generated is'.format(link))

                self.log.write_log("Data fetched from link")
                stock_data.dropna(inplace=True)
                self.log.write_log('Dropped null value')
                stock_data.reset_index(drop=True, inplace=True)
                stock_data['Date'] = pd.to_datetime(stock_data['Date'])
                self.log.write_log('Formatted the dataset')

                self.stock_open['Date'] = stock_data['Date']
                self.stock_open[self.stock[i]] = pd.Series(stock_data['Open'])
                self.log.write_log('Stock_open data frame created')

                self.stock_close['Date'] = stock_data['Date']
                self.stock_close[self.stock[i]] = stock_data['Close']
                self.log.write_log('stock_close dataframe created')

                self.stock_qnt[self.stock[i]] = pd.Series(int(investment / (len(self.stock) * stock_data['Open'][0])))
                self.log.write_log('stock_qnt dataframe created')

                self.stock_daily_val[self.stock[i]] = int(self.stock_qnt[self.stock[i]]) * self.stock_close[
                    self.stock[i]]
                self.log.write_log('stock_daily_val dataframe created')

                self.__stock_equity_curve['Date'] = stock_data['Date']
                self.__stock_equity_curve['EquityCurve'] = self.stock_daily_val.sum(axis=1)
                self.log.write_log('Equity curve dataframe created and returned')

            return self.__stock_equity_curve

        except:
            self.log.write_log( traceback.format_exc(), log_level='error')
            return traceback.format_exc()



    def stock_top_n(self, top, days_to_count=100):

        """
        Calculate top n stocks based on the past 100 days performance.

        :param top: Count of top n stocks
        :param days_to_count: No of days to count for evaluating performance of a stock. Default value is 100

        :return: List of top n stock based on past 100 days performance
        """
        self.log.write_log("Inside the method {}".format('stock_top_n'))
        self.log.write_log("Top parameter is {}".format(top))
        self.log.write_log("days_to_count parameter is {}".format(days_to_count))

        try:
            if top > len(self.stock):
                self.log.write_log("stock do not contain {} stocks. Add more stocks in list".format(int(top)))
                return "stock do not contain {} stocks. Add more stocks in list".format(int(top))

            stock_performance = pd.DataFrame()

            performance_start_date = int(self.start_date) - (days_to_count + 1) * 24 * 3600
            performance_end_date = int(self.start_date) - 24 * 3600

            self.log.write_log("Performance start date: {} , end date: {} ".format(performance_start_date,performance_end_date))
            for i in range(len(self.stock)):
                link1 = "https://query1.finance.yahoo.com/v7/finance/download/{0}?period1={1}&period2={2}&interval=1d&events=history&includeAdjustedClose=true".format(
                    self.stock[i] + '.NS', performance_start_date, (performance_start_date + 3600 * 24))
                link2 = "https://query1.finance.yahoo.com/v7/finance/download/{0}?period1={1}&period2={2}&interval=1d&events=history&includeAdjustedClose=true".format(
                    self.stock[i] + '.NS', (performance_end_date - 3600 * 24), performance_end_date)

                df1 = float(pd.read_csv(link1)['Close'])
                df2 = float(pd.read_csv(link2)['Close'])
                self.log.write_log("Data fetched")

                stock_performance[self.stock[i]] = pd.Series([df2, df1, df2 / df1])

            stock_performance = stock_performance.T
            stock_performance.columns = ['close_1', 'close_100', 'gain']
            self.log.write_log('Stock performance data frame created')

            stock_performance.sort_values(['gain'], inplace=True, ascending=False)

            stock_top_n_performance = stock_performance.head(top)
            self.log.write_log("Top {} performing stocks are{}".format(top, list(stock_top_n_performance.index)))

            return list(stock_top_n_performance.index)

        except:
            self.log.write_log( traceback.format_exc(), log_level='error')
            return traceback.format_exc()

    def CAGR(self, equity_curve):

        """
        Return the CAGR ratio
        :param equity_curve: DataFrame of equity curve defined in this Class
        :return: CAGR Ratio
        """
        self.log.write_log("Inside the method {}".format('CAGR'))
        self.log.write_log("Equity curve DataFrame".format(equity_curve.head(2)))
        try:
            y_begin = equity_curve['EquityCurve'][0]
            self.log.write_log('y_begin: {}'.format(y_begin))

            y_final = equity_curve['EquityCurve'][len(equity_curve) - 1]
            self.log.write_log('y_final: {}'.format(y_final))

            time_period = round((int(self.end_date) - int(self.start_date)) / (3600 * 24 * 365), 2)
            self.log.write_log('time_period: {}'.format(time_period))

            CAGR = (((y_final / y_begin) ** (1 / time_period)) - 1) * 100
            self.log.write_log('CAGR: {} is returned'.format(CAGR))

            return CAGR

        except:
            self.log.write_log( traceback.format_exc(), log_level='error')
            return traceback.format_exc()

    def votality(self, equity_curve):

        """
        :param equity_curve: DataFrame of equity curve defined in this Class
        :return: Volatility ratio
        """

        self.log.write_log("Inside the method {}".format('votality'))
        self.log.write_log("Equity curve DataFrame".format(equity_curve.head(2)))
        try:
            b = equity_curve['EquityCurve']
            c = pd.concat([pd.Series([1000000]), b])

            c.drop(c.tail(1).index, inplace=True)
            c.reset_index(drop=True, inplace=True)

            equity_curve['PreviousDayValue'] = c
            equity_curve['DailyReturn'] = ((equity_curve['EquityCurve'] / equity_curve['PreviousDayValue']) - 1)

            votality = (np.std(equity_curve['DailyReturn']) ** (1 / 252)) * 100
            self.log.write_log("Volatility is {}".format(votality))

            self.__Daily_return_std = np.std(equity_curve['DailyReturn'])
            self.__Daily_return_mean = np.mean(equity_curve['DailyReturn'])
            self.log.write_log("variable created __Daily_return_std: {} /n__Daily_return_mean: {} ".format(self.__Daily_return_std, self.__Daily_return_mean))

            return votality

        except:
            self.log.write_log(traceback.format_exc(), log_level='error')
            return traceback.format_exc()

    def sharpe_ratio(self):

        """
        NOTE: This can only be evaluated once the function volatility ratio is calculated.
        :return: Sharpe_ratio
        """
        self.log.write_log("Inside the method {}".format('sharpe_ratio'))
        try:
            ratio = (self.__Daily_return_std / self.__Daily_return_mean) ** (1 / 252)
            self.log.write_log('Sharpe_ratio is {} is returned'.format(ratio))
            return ratio

        except:
            self.log.write_log( traceback.format_exc(), log_level='error')
            return traceback.format_exc()
