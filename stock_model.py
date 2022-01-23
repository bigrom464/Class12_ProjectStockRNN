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


def formatDate(date):
    return date.split(' ')[0]


def getMaxDate(date):
    year = int(date.split('-')[0])
    month = int(date.split('-')[1])
    if month == 2:
        if year % 4 != 0:
            lastday = '28'
        else:
            lastday = '29'
    elif month <= 7 and month % 2 != 0 or month >= 8 and month % 2 == 0:
        lastday = '31'
    else:
        lastday = '30'
    date = date[:8] + lastday


def getPlotData(ticker, startDate, endDate):
    df = yf.download(ticker)  # get stock data from Yahoo! Finance
    # if not df.empty:
    df.to_csv(ticker+'.csv')
    df = pd.read_csv(ticker + '.csv', skiprows=[])
    df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d')  # format data
    df.index = df['Date']
    return df[startDate: endDate]


def getIPO(ticker='TSLA'):  # find first valid traded date on stock exchange
    df = yf.download(ticker)
    df.to_csv(ticker+'.csv')
    df = pd.read_csv(ticker+'.csv', skiprows=[])
    df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d')
    df.index = df['Date']
    return formatDate(str(df['Date'][0]))


def predict(ticker):
    rcParams['figure.figsize'] = 20, 10
    scaler = MinMaxScaler(feature_range=(0, 1))

    df = yf.download(ticker)  # get stock data from Yahoo! Finance
    df.to_csv(ticker+'.csv')
    df = pd.read_csv(ticker+'.csv', skiprows=[])
    df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d')  # format data
    df.index = df['Date']  # index data on date for plotting

    data = df.sort_index(ascending=True, axis=0)
    new_data = pd.DataFrame(index=range(0, len(df)), columns=['Date', 'Close'])
    for i in range(0, len(data)):
        new_data['Date'][i] = data['Date'][i]
        new_data['Close'][i] = data['Close'][i]

    new_data.index = new_data.Date
    new_data.drop('Date', axis=1, inplace=True)

    dataset = new_data.values
    # divide data into training and validation sets
    train = dataset[0: int(0.6 * len(df)), :]
    valid = dataset[int(0.6 * len(df)):, :]
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)  # pre-process data

    x_train, y_train = [], []
    for i in range(60, len(train)):
        x_train.append(scaled_data[i-60:i, 0])
        y_train.append(scaled_data[i, 0])
    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    # create data which is ready for model

    model = Sequential()  # create a sequential model
    model.add(LSTM(units=50, return_sequences=True,
              input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(units=50))  # add LSTM units
    model.add(Dense(1))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)

    inputs = new_data[len(new_data) - len(valid) - 60:].values
    inputs = inputs.reshape(-1, 1)
    inputs = scaler.transform(inputs)

    x_test = []
    for i in range(60, inputs.shape[0]):
        x_test.append(inputs[i-60:i, 0])
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    # use model to get predicted closing prices
    closing_price = model.predict(x_test)
    closing_price = scaler.inverse_transform(closing_price)
    rms = np.sqrt(np.mean(np.power((valid-closing_price), 2)))

    train = new_data[0: int(0.6 * len(df))]
    valid = new_data[int(0.6 * len(df)):]
    valid['Predictions'] = closing_price

    return train['Close'], valid[['Close', 'Predictions']]
