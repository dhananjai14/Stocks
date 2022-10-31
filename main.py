from flask import Flask, request, jsonify, render_template
from strategy import Stock
import pandas as pd
import matplotlib.pyplot as plt
from logger import logs

app = Flask(__name__)


@app.route('/test_GET', methods=['GET', 'POST'])
def test_get():
    if request.method == 'POST':
        logs.write_log('Request method is POST')
        start_date = request.json['start_date']
        end_date = request.json['end_date']
        invest = int(request.json['invested_amount'])
        top_n = request.json['top_n_stock']
        days_to_count = request.json['days_to_count']
        logs.write_log(f'''User passed \nstart Date: {start_date} \nend_date: {end_date}        
                        \ninvest: {invest} \ntop_n: {top_n} \ndays_to_count: {days_to_count}''')

        a = Stock(start_date=start_date, end_date=end_date, stock_list=['%5ENSEI'])
        equity_curve_nifty_index = a.portfolio_equity_curve(investment=invest)
        CAGR_nifty_index = a.CAGR(equity_curve_nifty_index)
        Volatility_nifty_index = a.votality(equity_curve_nifty_index)
        Sharpe_ratio_nifty_index = a.sharpe_ratio()
        logs.write_log('NIFTY equity curve, CAGR Volatility index, sharpe ratio calculated')

        a = Stock(start_date=start_date, end_date=end_date)
        equity_curve_benchmark = a.portfolio_equity_curve(investment=invest)
        CAGR_benchmark = a.CAGR(equity_curve_benchmark)
        Volatility_benchmark = a.votality(equity_curve_benchmark)
        Sharpe_ratio_benchmark = a.sharpe_ratio()
        logs.write_log('Benchmark stock equity curve, CAGR Volatility index, sharpe ratio calculated')

        a = Stock(start_date=start_date, end_date=end_date)
        top_n_stock = a.stock_top_n(int(top_n), days_to_count=days_to_count)
        a = Stock(start_date=start_date, end_date=end_date, stock_list=top_n_stock)
        equity_curve_top_n = a.portfolio_equity_curve(investment=invest)
        CAGR_top_n = a.CAGR(equity_curve_top_n)
        Volatility_top_n = a.votality(equity_curve_top_n)
        Sharpe_ratio_top_n = a.sharpe_ratio()
        logs.write_log('top n stock equity curve, CAGR Volatility index, sharpe ratio calculated')

        CAGR_lst = [CAGR_nifty_index, CAGR_benchmark, CAGR_top_n]
        Volatility = [Volatility_nifty_index, Volatility_benchmark, Volatility_top_n]
        Sharpe_ratio = [Sharpe_ratio_nifty_index, Sharpe_ratio_benchmark, Sharpe_ratio_top_n]
        final = pd.DataFrame({'CAGR %': CAGR_lst, 'Volatility %': Volatility, 'Sharpe': Sharpe_ratio},
                             index=['NIFTY', 'Equal Alloc Buy Hold', 'Performance_strat'])
        logs.write_log('Result created')

        plt.figure(figsize=(15, 8))
        plt.plot(equity_curve_top_n['Date'], equity_curve_top_n['EquityCurve'], color='pink',
                 label='equity_curve_top_n')
        plt.plot(equity_curve_benchmark['Date'], equity_curve_benchmark['EquityCurve'], color='r',
                 label='equity_curve_benchmark')
        plt.plot(equity_curve_nifty_index['Date'], equity_curve_nifty_index['EquityCurve'], color='b',
                 label='equity_curve_nifty_index')
        plt.legend()
        plt.xticks(rotation=45)
        logs.write_log('Plot created')


        return jsonify('top N stock: {} and final indices {}'.format(top_n_stock, final))
        # (This return the required details but not the plot)



        # return jsonify('top N stock: {} and final indices {}'.format(top_n_stock, final)), render_template('untitled1.html', name = plt.show())
        # (This returns the plot and not the details)



if __name__ == '__main__':
    app.run(port=5000)
