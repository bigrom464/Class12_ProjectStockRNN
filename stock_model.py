#import packages
import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler

from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM

import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
from matplotlib.figure import Figure

import yfinance as yf


def get_ipo(ticker='TSLA'): #find first valid traded date on stock exchange
    df = yf.download(ticker)
    df.to_csv(ticker+'.csv')
    df = pd.read_csv(ticker+'.csv',skiprows=[])
    df['Date'] = pd.to_datetime(df.Date,format='%Y-%m-%d')
    df.index = df['Date']
    str_date=str(df['Date'][0]).split(' ')[0].split('-')
    return str_date[1]+'/'+str_date[2]+'/'+str_date[0]

def predict(ticker):
    rcParams['figure.figsize'] = 20,10
    scaler = MinMaxScaler(feature_range=(0, 1))
    #ticker=input('Enter the ticker:')
    df = yf.download(ticker)#get stock data from Yahoo! Finance
    df.to_csv(ticker+'.csv')
    df = pd.read_csv(ticker+'.csv',skiprows=[])
    df['Date'] = pd.to_datetime(df.Date,format='%Y-%m-%d')#format data

    df.index = df['Date']#index data on date for plotting
    #plt.figure(figsize=(16,8))
    #plt.title(ticker+' Stock Data from IPO to Present')
    #plt.plot(df['Close'], label='Close Price History')
    #plt.show()
    data = df.sort_index(ascending=True, axis=0)
    new_data = pd.DataFrame(index=range(0,len(df)),columns=['Date', 'Close'])
    for i in range(0,len(data)):
        new_data['Date'][i] = data['Date'][i]
        new_data['Close'][i] = data['Close'][i]

    new_data.index = new_data.Date
    new_data.drop('Date', axis=1, inplace=True)

    dataset = new_data.values
    train=dataset[0:int(0.6*len(df)),:]#divide data into training and validation sets
    valid=dataset[int(0.6*len(df)):,:]
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)#pre-process data

    x_train, y_train = [], []
    for i in range(60,len(train)):
        x_train.append(scaled_data[i-60:i,0])
        y_train.append(scaled_data[i,0])
    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
    #create data which is ready for model

    model = Sequential()# create a sequential model 
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
    model.add(LSTM(units=50))# add LSTM units
    model.add(Dense(1))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)

    inputs = new_data[len(new_data) - len(valid) - 60:].values
    inputs = inputs.reshape(-1,1)
    inputs  = scaler.transform(inputs)

    X_test = []
    for i in range(60,inputs.shape[0]):
        X_test.append(inputs[i-60:i,0])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
    closing_price = model.predict(X_test)#use model to get predicted closing prices
    closing_price = scaler.inverse_transform(closing_price)
    rms=np.sqrt(np.mean(np.power((valid-closing_price),2)))
    train=new_data[0:int(0.6*len(df))]
    valid=new_data[int(0.6*len(df)):]
    valid['Predictions'] = closing_price
    return train['Close'],valid[['Close','Predictions']]
    #plt.title(ticker+' Prediction')
    #plt.plot(train['Close'])
    #plt.plot(valid[['Close','Predictions']])
    #plt.show()
