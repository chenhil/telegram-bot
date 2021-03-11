import requests
import re
import sys
import json

_yahoo_hostname = "https://finance.yahoo.com"
_default_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class StocksG(object):
    def __init__(self):
        self._hostname = ""
        self._request_url = ""
        self.stock_symbol = ""
        self.stock_data = {}

    def get_data(self, stock_symbol):
        pass

    def _request_stock_data(self, headers):
        try:
            response = requests.get(url=self._request_url, headers=headers)    
            if response.status_code == 200:
                return response.text
        except requests.exceptions.Timeout as err:
            print(err)
        except requests.exceptions.HTTPError as err:
            print(err)

        return {}

class YahooStocksG(StocksG):

    def __init__(self):
        super(YahooStocksG, self).__init__()
        self._hostname = _yahoo_hostname
        self._all_data = {}

    def get_data(self, stock_symbol):
        self.stock_symbol = stock_symbol
        self._request_url = self._make_url()
        self._raw_data = self._request_stock_data(_default_headers)
        self._parse_stock_data(self._raw_data)
        return self.stock_data

    def _make_url(self):
        return f"{self._hostname}/quote/{self.stock_symbol}"

    def _parse_stock_data(self, raw_data):
        try:
            filtered_data = re.search(r'QuoteSummaryStore.*?:(.*?),"FinanceConfigStore"', raw_data).group(1)
            self.all_data = json.loads(filtered_data)
            self.__write_to_log(self.all_data)

            parsed_data = dict()
            price = self._get_if_exist(self.all_data, ['price'])
            company_summary = self._get_if_exist(self.all_data, ['summaryProfile'])
            summary_detail = self._get_if_exist(self.all_data, ['summaryDetail'])
            
            has_pre_market_data = False
            has_post_market_data = False

            if 'fmt' in self._get_if_exist(price, ['preMarketPrice']):
                has_pre_market_data = True
            if 'fmt' in self._get_if_exist(price, ['postMarketPrice']):
                has_post_market_data = True

            parsed_data['has_pre_market_data'] = has_pre_market_data
            parsed_data['has_post_market_data'] = has_post_market_data


            parsed_data['symbol']                         = self._get_if_exist(self.all_data, ['symbol'])
            parsed_data['company_short_name']             = self._get_if_exist(price, ['shortName'])
            parsed_data['company_long_name']              = self._get_if_exist(price, ['longName'])
            parsed_data['company_profile'] = {
                'market_cap': self._get_if_exist(price, ['marketCap', 'fmt']),
                'sector': self._get_if_exist(company_summary, ['sector']),
                'full_time_employees': self._get_if_exist(company_summary, ['fullTimeEmployees']),
                'city': self._get_if_exist(company_summary, ['city']),
                'state': self._get_if_exist(company_summary, ['state']),
                'country': self._get_if_exist(company_summary, ['country']),
                'website': self._get_if_exist(company_summary, ['website']),
                'summary': self._get_if_exist(company_summary, ['longBusinessSummary']),
            }
            parsed_data['currency_symbol']                = self._get_if_exist(price, ['currencySymbol'])
            parsed_data['regular_market_price']           = self._get_if_exist(price, ['regularMarketPrice', 'fmt'])
            parsed_data['pre_market_price']               = self._get_if_exist(price, ['preMarketPrice', 'fmt'])
            parsed_data['post_market_price']              = self._get_if_exist(price, ['postMarketPrice', 'fmt'])
            parsed_data['market_open_price']              = self._get_if_exist(price, ['regularMarketOpen', 'fmt'])
            parsed_data['regular_market_low']             = self._get_if_exist(price, ['regularMarketDayLow', 'fmt'])
            parsed_data['regular_market_high']            = self._get_if_exist(price, ['regularMarketDayHigh', 'fmt'])
            parsed_data['regular_market_volume']          = self._get_if_exist(price, ['regularMarketVolume', 'fmt'])
            parsed_data['regular_market_change']          = self._get_if_exist(price, ['regularMarketChange', 'fmt'])
            parsed_data['regular_market_change_percent']  = self._get_if_exist(price, ['regularMarketChangePercent', 'fmt'])
            parsed_data['post_market_change']             = self._get_if_exist(price, ['postMarketChange', 'fmt'])
            parsed_data['post_market_change_percent']     = self._get_if_exist(price, ['postMarketChangePercent', 'fmt'])
            parsed_data['average_volume']                 = self._get_if_exist(summary_detail, ['averageVolume', 'fmt'])
            parsed_data['fifty_two_week_low']             = self._get_if_exist(summary_detail, ['fiftyTwoWeekLow', 'fmt'])
            parsed_data['fifty_two_week_high']            = self._get_if_exist(summary_detail, ['fiftyTwoWeekHigh', 'fmt'])

            self.stock_data = parsed_data
        except ValueError as err:
            print("Decoding JSON has failed:")
            print(err)

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