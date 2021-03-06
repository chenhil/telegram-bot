import robin_stocks

login = robin_stocks.robinhood.login("chn.hillman@gmail.com", "Sand071292")
print(robin_stocks.robinhood.stocks.get_quotes("AAPL"))