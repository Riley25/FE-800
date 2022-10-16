import os
import pandas as pd
import yfinance as yf   # https://pypi.org/project/yfinance/
print(os.getcwd())   



print("\n BEGIN PROGRAM")
print('-------------------')

# Go get the data. 
print('GETTING OPTIONS DATA (YaHoo!)')
TICKER = yf.Ticker("AAPL")



# get stock info
# INFO = TICKER.info

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
print("STACK IT! \n")
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


# WRITE TO EXCEL  
joined_df.to_excel('AAPL_OPTION_CHAIN_10-16-2022_138-dot-38.xlsx' , index = False)


print("PROGRAM COMPLETE!")
