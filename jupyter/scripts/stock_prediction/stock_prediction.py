import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# Download historical data
data = yf.download('AAPL', start='2020-01-01', end='2023-01-01')
data['Close'].plot(title='AAPL Closing Prices')
plt.show()