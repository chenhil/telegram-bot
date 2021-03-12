import requests
import re
import sys
import json
from api.stocksg_config.stocksg_configurator import StocksConfigurator

_yahoo_hostname = "https://finance.yahoo.com"
_default_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class StocksG(object):
    def __init__(self):
        self._hostname = ""
        self._request_url = ""
        self.stock_symbol = ""
        self.stock_data = dict()
        self.config_id = {}
        self.configurator = {}

    def get_data(self, stock_symbol):
        pass

    def _load_stocks_config(self):
        self.configurator = StocksConfigurator(self.config_id)

    def _request_stock_data(self, headers):
        try:
            response = requests.get(url=self._request_url, headers=headers)    
            if response.status_code == 200:
                return response.text
        except requests.exceptions.Timeout as err:
            logging.error(err)
        except requests.exceptions.HTTPError as err:
            logging.error(err)

        return {}

class YahooStocksG(StocksG):
    def __init__(self):
        super(YahooStocksG, self).__init__()
        self.config_id = "yahoo"
        self._load_stocks_config()
        self._hostname = _yahoo_hostname

    def get_data(self, stock_symbol):
        self.stock_symbol = stock_symbol
        self._request_url = self._make_url()
        response = self._request_stock_data(_default_headers)
        self._parse_stock_data(response)
        return self.stock_data

    def _make_url(self):
        return f"{self._hostname}/quote/{self.stock_symbol}"

    def _parse_stock_data(self, raw_data):
        try:
            json_data = re.search(r'QuoteSummaryStore.*?:(.*?),"FinanceConfigStore"', raw_data).group(1)
            external_data = json.loads(json_data)

            self.stock_data['symbol'] = external_data['symbol']
            self._set_market_hours_available(external_data)

            # Configurator gives us the internal_name -> external_name mapping
            attributes_map = self.configurator.name_mapping
            for attr_type in attributes_map:
                attr_names = attributes_map[attr_type]
                external_attributes = self._get_if_exist(external_data, [attr_type])

                for name in attr_names:
                    ext_name = attr_names[name]['external_name']
                    ext_value = self._get_if_exist(external_attributes, [ext_name])
                    
                    # use the formatted value if we can, otherwise use default.
                    if 'fmt' in ext_value:
                        self.stock_data[name] = ext_value['fmt']
                    else:
                        self.stock_data[name] = ext_value

        except ValueError as err:
            print("Decoding JSON has failed:")
            print(err)

    def _set_market_hours_available(self, external_data):
        price = self._get_if_exist(external_data, ['price'])
        # Check to see if there is pre/post market hours
        has_pre_market_data = False
        has_post_market_data = False
        if 'fmt' in self._get_if_exist(external_data, ['price', 'preMarketPrice']):
            has_pre_market_data = True
        if 'fmt' in self._get_if_exist(external_data, ['price', 'postMarketPrice']):
            has_post_market_data = True

        self.stock_data['has_pre_market_data'] = has_pre_market_data
        self.stock_data['has_post_market_data'] = has_post_market_data

    def _get_if_exist(self, map, keys):
        obj = map
        for key in keys:
            if key in obj:
                obj = obj[key]
            else:
                return ""

        return obj

    def __write_to_log(self, jsonObj):
        try:
            file_name = "logs.txt"
            file_out = open(file_name, "w")
            file_out.write(json.dumps(jsonObj, indent=2))
            file_out.close()
        except OSError:
            print("Could not write to file: ", file_name)
            sys.exit()