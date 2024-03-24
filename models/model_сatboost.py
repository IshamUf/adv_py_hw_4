import pandas as pd
from catboost import CatBoostRegressor
import datetime
import yfinance as yf
import numpy as np


def create_lags(df, lags):
    for i in range(1, lags + 1):
        df[f'lag_{i}'] = df['Close'].shift(i)
    df.dropna(inplace=True)
    return df


def get_data(ticket):
    ticker_tmp = ticket
    start = str(datetime.date(2018, 1, 1))
    end = str(datetime.date.today())
    stock = yf.download(ticker_tmp, start=start, end=end, interval="1D")
    if not stock.empty:
        return stock
    else:
        return None


def get_prediction_catboost(ticket, pred_days, lags=5):
    data = get_data(ticket)
    if data is not None:
        data_lagged = create_lags(data, lags)
        X = data_lagged.drop(['Open','High','Low','Close', 'Adj Close','Volume'], axis=1)
        y = data_lagged['Close']
        model = CatBoostRegressor(verbose=False)
        model.fit(X, y)
        last_observations = data_lagged.iloc[-lags:][['Close']]
        future_dates = pd.DataFrame([last_observations.values.flatten()])

        columns_name = []

        for i in range(lags):
            columns_name.append(f'lag_{i+1}')
        future_dates.columns = columns_name

        predictions = []

        for _ in range(pred_days):
            next_day_pred = model.predict(future_dates)
            predictions.append(next_day_pred[0])
            future_dates = np.roll(future_dates, -1)
            future_dates[0, -1] = next_day_pred[0]

        return predictions
    else:
        return None


# print(get_prediction_catboost('AAPL',5))
