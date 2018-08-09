from market_observer import Observable, AmericanMarket, EuropeanMarket

if __name__ == "__main__":
    trading_exchange = Observable()
    amc_market = AmericanMarket('Santa')
    eur_market = EuropeanMarket('Democracy')
    # Practice: create one more observer type - client
    trading_exchange.register(amc_market)
    trading_exchange.send_update('8am','GMT', dowjones=10125)
    trading_exchange.register(eur_market)
    trading_exchange.send_update('9am','GMT', dowjones=10129)

