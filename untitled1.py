# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JUU_B78v8STe7lesvUXvj3nDu3JkB5L7
"""

import pandas as pd
import numpy as np

import pandas_datareader.data as web
import datetime

start = datetime.datetime(2000,1,1)
end = datetime.datetime(2021,2,8)

code_Name = '^KS11'
code=web.DataReader(code_Name,"yahoo", start, end)
code

import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import math



data = code.filter(['Close']).values

scalar = MinMaxScaler(feature_range=(0,1))
scaled_data = scalar.fit_transform(data)
scaled_data

training_data_len = math.ceil(len(scaled_data)*0.8)
train_data = scaled_data[0:training_data_len]
train_data

x_train = []
y_train = []

PAST_SET = 10

for i in range(PAST_SET, len(train_data)):
  x_train.append(train_data[i-PAST_SET:i ,0])
  y_train.append(train_data[i,0])

x_train, y_train=np.array(x_train), np.array(y_train)

x_train=np.reshape(x_train,(x_train.shape[0], x_train.shape[1],1))


from keras.models import Sequential
from keras.layers import Dense, LSTM

x_train.shape[1]

model = Sequential()
model.add(LSTM(50, return_sequences=True,input_shape=(x_train.shape[1],1)))
model.add(LSTM(50,return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

model.compile(optimizer='adam',loss='mean_squared_error', metrics=['accuracy'])
model.fit(x_train,y_train,batch_size =1, epochs =50)

test_data= scaled_data[training_data_len - PAST_SET:,:]

x_test = []
y_test = data[training_data_len:,:]
for i in range(PAST_SET,len(test_data)):
  x_test.append(test_data[i-PAST_SET:i,0])

x_test=np.array(x_test)
x_test = np.reshape(x_test,(x_test.shape[0], x_test.shape[1], 1))

predictions = model.predict(x_test)
predictions = scalar.inverse_transform(predictions)

rmse = np.sqrt(np.mean(predictions - y_test)**2)
rmse

data = code.filter(['Close'])

train=data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions']= predictions

plt.figure(figsize=(18,9))
plt.plot(train['Close'])
plt.plot(valid[['Close','Predictions']])
plt.legend(['Train','Val','Predictions'],loc='low')