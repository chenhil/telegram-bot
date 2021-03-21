from bs4 import BeautifulSoup
from graphqlclient import GraphQLClient
from decimal import *
from millify import millify, prettify
import time, json, logging, requests, json


class Uniswap():

    Tokens = dict()

    def __init__(self):
        if len(self.Tokens) == 0:
            self._getAllToken()
        self.graphqlClientUni = GraphQLClient(endpoint="https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2")
        self.graphqlClientEth = GraphQLClient('https://api.thegraph.com/subgraphs/name/blocklytics/ethereum-blocks')
        self.query_eth = '''query blocks {
            t1: blocks(first: 1, orderBy: timestamp, orderDirection: desc, where: {timestamp_gt: %d, timestamp_lt: %d}) {
                    number
            }
            t2: blocks(first: 1, orderBy: timestamp, orderDirection: desc, where: {timestamp_gt: %d, timestamp_lt: %d}) {
                    number
            }
            t3: blocks(first: 1, orderBy: timestamp, orderDirection: desc, where: {timestamp_gt: %d, timestamp_lt: %d}) {
                    number
            }            
            tnow: blocks(first: 1, orderBy: timestamp, orderDirection: desc, where: {timestamp_lt: %d}) {
                    number
            }
        }'''
        self.query_uni = '''query blocks {
            t1: token(id: "CONTRACT", block: {number: NUMBER_T1}) {
                derivedETH
            }
            t2: token(id: "CONTRACT", block: {number: NUMBER_T2}) {
                derivedETH
            }
            t3: token(id: "CONTRACT", block: {number: NUMBER_T3}) {
                derivedETH
            }            
            tnow: token(id: "CONTRACT", block: {number: NUMBER_TNOW}) {
                derivedETH
            }
            b1: bundle(id: "1", block: {number: NUMBER_T1}) {
                ethPrice
            }
            b2: bundle(id: "1", block: {number: NUMBER_T2}) {
                ethPrice
            }
            b3: bundle(id: "1", block: {number: NUMBER_T3}) {
                ethPrice
            }            
            bnow: bundle(id: "1", block: {number: NUMBER_TNOW}) {
                ethPrice
            }
        }
        '''        

    def getPriceUniswap(self, symbol):
        if symbol not in self.Tokens:
            return None

        address = self.Tokens[symbol]
        response = {}
        now = int(time.time())

        before_1h = now - 3600
        before_1h_high = before_1h + 600

        before_7d = now - 3600 * 24 * 7
        before_7d_high = before_7d + 600

        before_1d = now - 3600 * 24
        before_1d_high = before_1d + 600

        updated_eth_query = self.query_eth % (before_7d, before_7d_high, before_1d, before_1d_high, before_1h, before_1h_high, now)
        res_eth_query = self.graphqlClientEth.execute(updated_eth_query)
        json_resp_eth = json.loads(res_eth_query)
        
        block_from_7d = int(json_resp_eth['data']['t1'][0]['number'])
        block_from_1d = int(json_resp_eth['data']['t2'][0]['number'])
        block_from_1h = int(json_resp_eth['data']['t3'][0]['number'])
        latest_block = int(json_resp_eth['data']['tnow'][0]['number'])

        query_uni_updated = self.query_uni.replace("CONTRACT", address) \
            .replace("NUMBER_T1", str(block_from_7d)) \
            .replace("NUMBER_T2", str(block_from_1d)) \
            .replace("NUMBER_T3", str(block_from_1h)) \
            .replace("NUMBER_TNOW", str(latest_block))

        res_uni_query = self.graphqlClientUni.execute(query_uni_updated)
        json_resp_uni = json.loads(res_uni_query)

        try:
            per_eth_7d = float(json_resp_uni['data']['t1']['derivedETH'])
        except KeyError:  
            last_block_indexed = str(res_uni_query).split('indexed up to block number ')[1][0:8]
            query_uni_updated = self.query_uni.replace("CONTRACT", address) \
                .replace("NUMBER_T1", str(block_from_7d)) \
                .replace("NUMBER_T2", str(block_from_1d)) \
                .replace("NUMBER_T3", str(block_from_1h)) \
                .replace("NUMBER_TNOW", str(last_block_indexed))
            res_uni_query = self.graphqlClientUni.execute(query_uni_updated)
            json_resp_uni = json.loads(res_uni_query)
            per_eth_7d = float(json_resp_uni['data']['t1']['derivedETH'])

        # per_eth_7d = float(json_resp_uni['data']['t1']['derivedETH'])
        per_eth_1d = float(json_resp_uni['data']['t2']['derivedETH'])
        per_eth_1h = float(json_resp_uni['data']['t3']['derivedETH'])
        per_eth_now = float(json_resp_uni['data']['tnow']['derivedETH'])
        eth_price_7d = float(json_resp_uni['data']['b1']['ethPrice'])
        eth_price_1d = float(json_resp_uni['data']['b2']['ethPrice'])
        eth_price_1h = float(json_resp_uni['data']['b3']['ethPrice'])
        eth_price_now = float(json_resp_uni['data']['bnow']['ethPrice'])

        price7dUsd = per_eth_7d * eth_price_7d
        price1dUsd = per_eth_1d * eth_price_1d
        price1hUsd = per_eth_1h * eth_price_1h
        priceNowUsd = per_eth_now * eth_price_now

        var_7d = round(float(((priceNowUsd - price7dUsd) / priceNowUsd) * 100), 2)
        var_7d_str = str(var_7d) + "%" if var_7d > 0 else str(var_7d) + "%"
        var_1d = round(float(((priceNowUsd - price1dUsd) / priceNowUsd) * 100), 2)
        var_1d_str = str(var_1d) + "%" if var_1d > 0 else str(var_1d) + "%"
        var_1h = round(float(((priceNowUsd - price1hUsd) / priceNowUsd) * 100), 2)
        var_1h_str = str(var_1h) + "%" if var_1h > 0 else str(var_1h) + "%"

        response['price7d_usd'] = price7dUsd
        response['price1d_usd'] = price1dUsd
        response['price1h_usd'] = price1hUsd
        response['price'] = "$" + str(round(priceNowUsd, 6))
        response['percentChange1h'] = var_1h_str
        response['percentChange24h'] = var_1d_str
        response['percentChange7d'] = var_7d_str
        response['symbol'] = symbol
    
        return response

    def _getAllToken(self):
        try:
            response = requests.get('https://tokens.coingecko.com/uniswap/all.json')
            response.raise_for_status()
            jsonResponse = json.loads(response.content.decode('utf-8'))
            for tokeninfo in jsonResponse['tokens']:
                self.Tokens[tokeninfo['symbol']] = tokeninfo['address']
        except Exception as e:
            logging.error(e)
            raise e
