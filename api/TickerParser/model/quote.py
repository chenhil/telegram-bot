

class Quote:
    def __init__(self, symbol, price, volume24, percentChange1h, percentChange24h, percentChange7d, priceLow, priceHigh, marketCap):
        self.symbol = symbol
        self.price = price
        self.volume24 = volume24
        self.percentChange1h = percentChange1h
        self.percentChange24h = percentChange24h
        self.percentChange7d = percentChange7d
        self.priceLow = priceLow
        self.priceHigh = priceHigh
        self.marketCap = marketCap

    def getSymbol(self):
        return "{}    {}".format(self.symbol, self.price)

    def getPercentChange1h(self):
        return "1h:          {}".format(self.percentChange1h).replace(" -", "-")
    
    def getPercentChange24h(self):
        return "24h:         {}".format(self.percentChange24h).replace(" -", "-")

    def getPercentChange7d(self):
        return "7d:          {}".format(self.percentChange7d).replace(" -", "-")
    
    def getVolume(self):
        return "Volume24h:   {}".format(self.volume24)

    def getPriceLowHigh(self):
        return "24h Low/ 24h High: {}/{}".format(self.priceLow, self.priceHigh)

    def getMarketCap(self):
        return "Market Cap:  {}".format(self.marketCap)

    def getMarkdown(self):
        output = (str('```') + "\n" + self.getSymbol() + "\n" 
        + self.getPercentChange1h() + "\n" 
        + self.getPercentChange24h() + "\n" 
        + self.getPercentChange7d() + "\n" 
        + self.getPriceLowHigh() + "\n"
        + self.getVolume() + "\n"
        + self.getMarketCap() + "\n"
        + str('```'))

        return output.replace(".", "\\.").replace("-", "\\-").replace("|", "\\|")
