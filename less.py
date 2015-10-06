import pandas as pd
import os
import time
from datetime import datetime

path = "/Users/ae9693/Desktop/Programming/python/yt/intraQuarter"
def Key_Stats(gather = "Total Debt/Equity (mrq)"):
    statspath = path +('/_KeyStats')
    stock_list = [x[0] for x in os.walk(statspath)] # this are all the folders
    df = pd.DataFrame(columns = ['Date',
                                'Unix',
                                 'Ticker',
                                 'De Ratio',
                                 'Price',
                                 'stock_p_change',
                                 'SP500',
                                 'sp500_p_change'])

    sp500_df = pd.DataFrame.from_csv('YAHOO-INDEX_GSPC.csv')
    ticker_list = list()
    for folder in stock_list[1:15]:
        each_file = os.listdir(folder)

        ticker = folder.split("/")[-1]
        ticker_list.append(ticker)

        starting_stock_value = False
        starting_sp500_value = False

        if len(each_file) > 0:
            for file in each_file[1:]:      # there is some weird value at [0]
                # print file
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                # print unix_time
                full_file_path = folder + '/' + file
                # print full_file_path
                source = open(full_file_path, 'r').read()  # opening a file for reading
                try:
                    value = float(source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])

                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adjusted Close"])
                    except Exception as e:
                        sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adjusted Close"])

                    stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])

                    print "stock_price:", stock_price, "ticker:", ticker


                    # handle if
                    if not starting_stock_value:
                        starting_stock_value = stock_price
                    if not starting_sp500_value:
                        starting_sp500_value = sp500_value
                    #calculate % change
                    stock_p_change = ((stock_price - starting_stock_value) /starting_stock_value) *100
                    sp500_p_change = ((sp500_value - starting_sp500_value) /starting_sp500_value) *100

                    # compare the change
                    stock_p_change - sp500_p_change


                    # append to dict
                    df = df.append({'Date': date_stamp,
                                    'Unix': unix_time,
                                    'Ticker': ticker,
                                    'De Ratio': value,
                                    'Price': stock_price,
                                    'stock_p_change': stock_p_change,
                                    'SP500': sp500_value,
                                    'sp500_p_change': sp500_p_change
                                    }, ignore_index=True)

                except Exception as e:
                    # print e
                    pass
    save = gather.replace(' ', '').replace('(', '').replace(')', '').replace('/', '')+'.csv'
    #print(save)
    df.to_csv(save)


Key_Stats()