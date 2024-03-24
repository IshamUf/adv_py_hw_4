from models.model_arima import get_prediction_arima
from models.model_сatboost import get_prediction_catboost
from fastapi import FastAPI
import aioredis
from horoscope import get_horoscope
from datetime import datetime

app = FastAPI()

model = ['Arima', 'Catboost']


redis = None


@app.on_event("startup")
async def startup_event():
    global redis
    redis = aioredis.from_url("redis://redis")


async def check_cache(ticket: str, days: int):
    key = ticket + str(days)
    value = await redis.get(key)
    if value is not None:
        return value
    else:
        return None


async def save_cache(ticket: str, days: int, data):
    key = ticket + str(days)
    await redis.set(key, data, ex=30)


def pars_res(lst, days, ticket, model_name):
    if lst is None:
        return f'ОШИБКА: ТАКОГО ТИКЕТА <{ticket}> НЕТ В БАЗЕ'
    else:
        ans = f'Предсказания от модели {model_name} ->  '
        for i in range(days):
            ans += f"День {i + 1}: {lst[i]}; "
        return ans


@app.get("/ping")
async def ping_point():
    return 'pong'


@app.get("/help")
async def help_point():
    ans = "Доступные модели: arima (/arima/{ticket} или /arima/{ticket}/{days}), catboost (/cat?ticket=AAPL&days=3)" \
          "Для методов без указания дней, количество дней является 5"
    return ans


async def arima_pred(ticket,days):
    value = await check_cache(ticket, days)
    if value is None:
        print("Кеша нет")
        res = pars_res(get_prediction_arima(ticket, days), days, ticket, model[0])
        await save_cache(ticket, days, res)
        return res
    else:
        print("Кеш есть")
        return value


@app.get("/arima/{ticket}")
async def arima(ticket: str, days: int = 5):
    res = await arima_pred(ticket,days)
    return res


@app.get("/arima/{ticket}/{days}")
async def arima_days(ticket: str, days: int):
    res = await arima_pred(ticket, days)
    return res


@app.get("/cat")
async def cat(ticket: str = "AAPL", days: int = 5):
    value = await check_cache(ticket, days)
    if value is None:
        print("Кеша нет")
        res = pars_res(get_prediction_catboost(ticket, days), days, ticket, model[1])
        await save_cache(ticket, days, res)
        return res
    else:
        print("Кеш есть")
        return value


@app.get("/horoscope")
async def my_horoscope(sign: str = None):
    value = await check_cache(str(sign), datetime.now().day)
    if value is None:
        print("Кеша нет")
        text = get_horoscope(sign)
        await save_cache(str(sign), datetime.now().day, text)
        return text
    else:
        print("Кеш есть")
        return value


@app.on_event("shutdown")
async def shutdown_event():
    global redis
    await redis.close()