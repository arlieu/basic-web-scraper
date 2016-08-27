
import requests
from bs4 import BeautifulSoup
import sys
import re

class WebScraper:
    statistics = {}

    def __init__(self):
        self.Selection()

    def Selection(self):
        targets = []
        n = 0

        print("Enter the symbols for the stock you would like to view." +
	    "\nEnter 'end' when all stocks have been input.")

        end = False
        while (not end):
            symbol = input("Symbol " + str(n+1) + ": ").lower()
            if (symbol == "end"):
                if (len(targets) == 0):
                    print("No valid symbol entered.")
                    restart = input("Do you wish to continue (Y/n)? ").upper()
                    if (restart == "YES" or restart == "Y"):
                        continue
                    elif (restart == "NO" or restart == "N"):
                        print("Program terminated.")
                        sys.exit(0)
                    else:
                        print("Invalid response.")
                        continue
                end = True
            elif (self.ValidSymbol(symbol)):   
                targets.append(symbol)
                n += 1
            else:
                continue
            
        self.StockInfo(targets, n)

    def ValidSymbol(self, symbol): 
        url = "http://www.nasdaq.com/symbol/" + symbol
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        invalid = soup.find("div", {"class": "notTradingIPO"}) 
        if (not invalid):
            print("Valid")
            return True
        else: 
            print("Invalid symbol")
            return False

    def StockInfo(self, targets, n):
        # NASDAQ summary data is collected and stored for each valid symbol.
        labels = ["Bid/Ask", "1 Year Target Price", "---", "Share Volume", "---", "---", "52 Week High/Low", 
                    "Market Cap", "P/E", "---", "EPS", "---", "---", "---", "---", "Beta", "---", "---", 
                    "---", "---", "---"]
        for i in range(0, n):                 
            url = "http://www.nasdaq.com/symbol/" + targets[i]
            r = requests.get(url)
                
            soup = BeautifulSoup(r.content, "html.parser")      #  html data parsed for reading

            # No unique identifiers for tds' containing summary data.
            # DOM positioning used to identify relevant data.
            table = soup.find("table", {"class": "widthF"})
            nestedTable = table.find("table")
                
            cnt = 0
            for td in nestedTable.find_all("td", {"align": "right"}):
                self.statistics[labels[cnt]] = re.sub('[^0-9./]', '', str(td.contents))
                cnt += 1
            del self.statistics["---"]
        print(self.statistics)

    #def Prices(self, targets, n):
        