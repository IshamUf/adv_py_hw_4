import pandas as pd
import yfinance as yf
import datetime
from statsmodels.tsa.arima.model import ARIMA


def get_data(ticket):
    ticker_tmp = ticket
    start = str(datetime.date(2018, 1, 1))
    end = str(datetime.date.today())
    stock = yf.download(ticker_tmp, start=start, end=end, interval="1D")
    if not stock.empty:
        train = stock['Adj Close']
        train.index = pd.DatetimeIndex(train.index).to_period('D')
        return train
    else:
        return None


def find_params_aic(data, p_range, d_range, q_range):
    best_aic, best_cfg = float("inf"), None
    for p in p_range:
        for d in d_range:
            for q in q_range:
                order = (p, d, q)
                try:
                    model = ARIMA(data, order=order)
                    model_fit = model.fit()
                    aic = model_fit.aic
                    if aic < best_aic:
                        best_aic, best_cfg = aic, order
                except:
                    continue
    return best_cfg, best_aic


def get_prediction_arima(ticket, days):
    train = get_data(ticket)
    if train is not None:
        best_params = find_params_aic(train, range(1, 3), range(1, 2), range(1, 3))
        model = ARIMA(train, order=best_params[0])
        model_fit = model.fit()
        model_fit.aic
        forecast_result = model_fit.get_forecast(steps=days)
        forecast_mean = forecast_result.predicted_mean
        return list(forecast_mean)
    else:
        return None


# pred, params = get_prediction_arima('AAPL')
#
# print(pred)
#
# print(params)

