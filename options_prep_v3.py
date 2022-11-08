import os
import pandas as pd
import numpy as np  
import yfinance as yf          # https://pypi.org/project/yfinance/
from datetime import datetime, timedelta

ticker = 'AAPL'

print(' ')
print("BEGIN PROGRAM .... " + ticker + ' Data')
print('----------------------------- \n')


now = datetime.now() + timedelta(days = 1) 
end_date = now.strftime("%Y-%m-%d")
start_date = (now - timedelta(days = 5)).strftime("%Y-%m-%d")

print(end_date)



# Most recent stock price
SP = yf.download( tickers = ticker,   
                    start=start_date, 
                    end=end_date,
                    interval = "1d", 
                    auto_adjust = True  )    

SP  = SP[['Close']]
SP = SP.reset_index()
max_date = np.max(SP['Date'])  
print(max_date)

print(SP)
last_known_price = str( float( np.round( SP[SP['Date'] == max_date]['Close'] , decimals = 5 ) ) )
print('THE MOST CURRENT STOCK PRICE = $ ' + str(last_known_price))



# Get options data. 
print('GETTING OPTIONS DATA (YaHoo!) \n')
TICKER = yf.Ticker(ticker)


dates = TICKER.options
l = len(dates)

call_col_names = TICKER.option_chain(dates[0]).calls.columns
put_col_names = TICKER.option_chain(dates[0]).puts.columns

# START AN EMPTY DATA FRAME
stacked_call_data = pd.DataFrame(columns =  call_col_names)
stacked_call_data['OPTION_TYPE'] = []
stacked_call_data['EXPIRATION_DATE']  = []

stacked_put_data = pd.DataFrame(columns =  put_col_names)
stacked_put_data['OPTION_TYPE'] = []
stacked_put_data['EXPIRATION_DATE']  = []


# STACK THE DATASETS
#print("STACK IT! \n")
for i in range(0, l):

    OPTIONS_d = TICKER.option_chain(dates[i])

    temp_call_df = OPTIONS_d.calls
    call_rows, call_columns = temp_call_df.shape


    temp_put_df = OPTIONS_d.puts
    put_rows, put_columns = temp_put_df.shape


    temp_call_df['OPTION_TYPE'] = ['CALLS'] * call_rows
    temp_call_df['EXPIRATION_DATE'] = [dates[i]] * call_rows

    temp_put_df['OPTION_TYPE'] = ['PUTS'] * put_rows
    temp_put_df['EXPIRATION_DATE'] = [dates[i]] * put_rows


    stacked_call_data = stacked_call_data.append( temp_call_df )
    stacked_put_data = stacked_put_data.append( temp_put_df )


# MERGE CALL AND PUTS
print('DATA PREP \n')
joined_df = pd.merge(stacked_call_data, stacked_put_data, left_on = ['strike', 'EXPIRATION_DATE'], right_on = ['strike', 'EXPIRATION_DATE'], how = 'inner', suffixes=('_CALL', '_PUT'))


# DATA CLEANING AND PREP
joined_df['SNAPSHOT_DATE'] = pd.to_datetime("today").strftime("%Y-%m-%d")    #  when was data collected? 
joined_df['SNAPSHOT_DATE'] = pd.to_datetime(joined_df['SNAPSHOT_DATE'])

joined_df['EXPIRATION_DATE'] = pd.to_datetime(joined_df['EXPIRATION_DATE'])  

joined_df['TIME_TO_MATURITY_(YRS)'] = joined_df['EXPIRATION_DATE'] - joined_df['SNAPSHOT_DATE'] 
joined_df['TIME_TO_MATURITY_(YRS)'] = joined_df['TIME_TO_MATURITY_(YRS)'].dt.days / 252

joined_df['mid_price_CALL'] = (joined_df['bid_CALL'] + joined_df['ask_CALL'])/2
joined_df['mid_price_PUT'] = (joined_df['bid_PUT'] + joined_df['ask_PUT'])/2



# SELECT A SUBSET OF COLUMNS
joined_df = joined_df[['contractSymbol_CALL' ,  'strike'  , 'bid_CALL', 'ask_CALL', 'mid_price_CALL', 'volume_CALL', 'openInterest_CALL', 'impliedVolatility_CALL', 'inTheMoney_CALL', 
                       'contractSymbol_PUT'  ,               'bid_PUT', 'ask_PUT',  'mid_price_PUT',  'volume_PUT' , 'openInterest_PUT' , 'impliedVolatility_PUT' , 'inTheMoney_PUT' , 
                       'EXPIRATION_DATE', 'SNAPSHOT_DATE' ,  'TIME_TO_MATURITY_(YRS)' ]]


# RENAME THE COLUMNS
joined_df.columns = ['CONTRACT_SYMBOL_CALL' ,  'STRIKE'  , 'BID_CALL', 'ASK_CALL', 'MID_PRICE_CALL', 'VOLUME_CALL', 'OPEN_INTEREST_CALL', 'IMPLIED_VOLATILITY_CALL', 'IN_THE_MONEY_CALL', 
                     'CONTRACT_SYMBOL_PUT'  ,             'BID_PUT', 'ASK_PUT',  'MID_PRICE_PUT',  'VOLUME_PUT' , 'OPEN_INTEREST_PUT' , 'IMPLIED_VOLATILITY_PUT' , 'IN_THE_MONEY_PUT' , 
                     'EXPIRATION_DATE', 'SNAPSHOT_DATE' ,  'TIME_TO_MATURITY_(YRS)' ]

n_row, n_col = joined_df.shape

# INCLUDE THE LAST KNOWN STOCK PRICE
joined_df.insert( (n_col ), 'STOCK_PRICE' ,  [float(last_known_price)]*n_row )


# WRITE TO EXCEL  
max_date = max_date.strftime('%Y-%m-%d')
joined_df.to_excel(ticker + '__' + str(max_date)  +'.xlsx', index = False)


print("PROGRAM COMPLETE!")







