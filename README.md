# adv_py_hw_4
Выполнение 4 домашнего задания. FastAPI, Redis, Docker.
Методы:
* /ping ответ pong - метод для тестировния FastAPI.
* /help - текст с информацией о методах.
* /arima/{ticket} - Метод предсказывания цен на акции на пять дней в зависимости от тикета. Пример: /arima/AAPL.
* /arima/{ticket}/{days} - Метод предсказывания цен на акции с помощью модели ARIMA в зависимости от тикета с возможность выбора кол-во дней. Пример: /arima/AAPL/3.
* /cat - Метод предсказывания цен на акции с помощью модели CATBOOST в зависимости от тикета с возможность выбора кол-во дней. Пример: /cat?ticket=AAPL&days=2.
* /horoscope - Метод позволяющий узнать гороскоп на каждый день. При указании знака зодиака предоставляет гороскоп учитывая знак. Пример: /horoscope&sign=leo.

Знаки зодиак: Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius, Capricorn, Aquarius, Pisces.

*main.py - основной код FastApi.\
*Horoscope.py - код для парсинга гороскопов.\
*model_arima.py - код для ARIMA модели.\
*model_catboost.py - код для CATBOOST модели.

http://94.198.218.216:8000/ - развернутый работающий сервис
