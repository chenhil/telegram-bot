import logging

from api.coingecko import CoinGecko
from api.uniswap import Uniswap
from api.coinpaprika import CoinPaprika

class Cache(object):
    cg_coinlist = list()
    cg_coinMarketList = dict()
    paprika_coinlist = dict()
    uniswap_coinlist = list()

    @staticmethod
    def refresh(bot):
        logging.info("Starting Caching")

        Cache.refresh_coingecko_coin_list()
        Cache.refresh_coinpaprika_coin_list()
        Cache.refresh_uniswap_coin_list()
        Cache.refresh_coingecko_market_list()

        logging.info("Finished Caching")

    @staticmethod
    def refresh_coingecko_coin_list():
        # Cache.cg_coinlist = CoinGecko().getCoinList()
        try: 
            coinlist = CoinGecko().getCoinList()
            Cache.cg_coinlist = coinlist
        except Exception as e:
            logging.error("Unable to refresh coingecko coinlist", e)


    @staticmethod
    def refresh_coinpaprika_coin_list():
        try:
            coinlist = CoinPaprika().getCoinList()
            Cache.paprika_coinlist = coinlist
        except Exception as e:
            logging.error("Unable to refresh coinpaprika coinlist", e)        

    @staticmethod
    def refresh_uniswap_coin_list():
        # Cache.uniswap_coinlist = Uniswap().getCoinList()     
        try:
            coinlist = Uniswap().getCoinList()     
            Cache.uniswap_coinlist = coinlist
        except Exception as e:
            logging.error("Unable to refresh uniswap coinlist", e)               

    @staticmethod
    def refresh_coingecko_market_list():
        try:
            coinlist = CoinGecko().getMarketData() 
            Cache.cg_coinMarketList = coinlist
        except Exception as e:
            logging.error("Unable to refresh coingecko marketdata", e)      

    @staticmethod
    def get_coingecko_list():
        return Cache.cg_coinlist

    @staticmethod
    def get_coinpaprika_list():
        return Cache.paprika_coinlist

    @staticmethod
    def get_coingecko_marketlist():
        return Cache.cg_coinMarketList

    @staticmethod
    def get_uniswap_list():
        return Cache.uniswap_coinlist
