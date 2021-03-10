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
        return f"{self._hostname}/quote/{self.stock_symbol}?p={self.stock_symbol}"

    def _parse_stock_data(self, raw_data):
        try:
            filtered_data = re.search(r'QuoteSummaryStore.*?:(.*?),"FinanceConfigStore"', raw_data).group(1)
            self.all_data = json.loads(filtered_data)
            self.__write_to_log(self.all_data)

            parsed_data = dict()
            price = self.all_data['price']
            company_summary = self.all_data['summaryProfile']
            summary_detail = self.all_data['summaryDetail']
            
            has_pre_market_hours = False
            has_post_market_hours = False

            if 'fmt' in price['preMarketPrice']:
                parsed_data['has_pre_market_data'] = True
                has_pre_market_hours = True
            else:
                parsed_data['has_pre_market_data'] = False
            if 'fmt' in price['postMarketPrice']:
                parsed_data['has_post_market_data'] = True
                has_post_market_hours = True
            else:
                has_post_market_hours = False

            parsed_data['symbol']                         = self.all_data['symbol']
            parsed_data['company_short_name']             = price['shortName']
            parsed_data['company_long_name']              = price['longName']
            parsed_data['company_profile'] = {
                'market_cap': price['marketCap']['fmt'],
                'sector': company_summary['sector'],
                'full_time_employees': company_summary['fullTimeEmployees'],
                'city': company_summary['city'],
                'state': company_summary['state'],
                'country': company_summary['country'],
                'website': company_summary['website'],
                'summary': company_summary['longBusinessSummary'],
            }
            parsed_data['currency_symbol']                 = price['currencySymbol']
            parsed_data['regular_market_price']           = price['regularMarketPrice']['fmt']
            if has_pre_market_hours:
                parsed_data['pre_market_price']           = price['preMarketPrice']['fmt']
            if has_post_market_hours:
                parsed_data['post_market_price']          = price['postMarketPrice']['fmt']
            if 'fmt' in price['regularMarketOpen']:
                parsed_data['market_open_price']          = price['regularMarketOpen']['fmt']
            parsed_data['regular_market_low']             = price['regularMarketDayLow']['fmt']
            parsed_data['regular_market_high']            = price['regularMarketDayHigh']['fmt']
            parsed_data['regular_market_volume']          = price['regularMarketVolume']['fmt']
            parsed_data['regular_market_change']          = price['regularMarketChange']['fmt']
            parsed_data['regular_market_change_percent']  = price['regularMarketChangePercent']['fmt']
            if has_post_market_hours:
                parsed_data['post_market_change']         = price['postMarketChange']['fmt']
            if has_post_market_hours:
                parsed_data['post_market_change_percent'] = price['postMarketChangePercent']['fmt']
            parsed_data['average_volume']                 = summary_detail['averageVolume']['fmt']
            parsed_data['fifty_two_week_low']             = summary_detail['fiftyTwoWeekLow']['fmt']
            parsed_data['fifty_two_week_high']            = summary_detail['fiftyTwoWeekHigh']['fmt']

            self.stock_data = parsed_data
        except ValueError as err:
            print("Decoding JSON has failed:")
            print(err)

    
    def __write_to_log(self, jsonObj):
        try:
            file_name = "logs.txt"
            file_out = open(file_name, "w")
            file_out.write(json.dumps(jsonObj, indent=2))
            file_out.close()
        except OSError:
            print("Could not write to file: ", file_name)
            sys.exit()