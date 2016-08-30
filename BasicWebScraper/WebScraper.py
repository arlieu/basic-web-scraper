import requests
from bs4 import BeautifulSoup
import sys
import re

class WebScraper:
    stocks = {} 

    def __init__(self):
        self.MainMenu()

    def MainMenu(self):
        '''Main menu options.'''
        print("Stock Data Extraction Tool\n" + \
            "--------------------------\n")
        while (1):
            print("Main Menu\n" + \
                "a) View Statistical Data\n" + \
                "b) Add Symbols to Portfolio\n" + \
                "c) Quit\n")
            
            selection = input("Please select an option: ").upper()
            print("")
            if (selection == 'A' or selection == "VIEW STATISTICAL DATA"):
                self.StatOptions()
            elif (selection == 'B' or selection == "ADD SYMBOLS TO PORTFOLIO"):
                self.MainMenu()
            elif (selection == 'C' or selection == "QUIT"): 
                print("Program terminated.")
                sys.exit(0)
            else:
                print("Invalid option.")
                continue
                
    def StatOptions(self):
        '''Options to view saved companies' statistical data.'''
        targets = []

        print("Statistical Data\n" + \
            "a) Current Price\n" + \
            "b) Bid/Ask\n" + \
            "c) 1 Year Target Price\n" + \
            "d) 52 Week High/Low\n" + \
            "e) Market Cap\n" + \
            "f) P/E\n" + \
            "g) EPS\n" + \
            "h) Beta\n")
        option = input("Please select an option: ").upper()
        
        print("\nEnter the symbols for the stocks you would like to view.\n" + \
            "Enter 'end' when all symbols have been input.")

        n = 1
        while (1):
            symbolSelection = input("Symbol " + str(n) + ": ")
            if (symbolSelection == "end"):
                if (len(targets) == 0):
                    print("No symbol entered.")
                    self.Redirect()
                else:
                    break
            elif (self.SavedSymbol(symbolSelection)):   
                targets.append(symbolSelection)
                n += 1
            else:
                print("Stock information not saved.")
                while (1):
                    addSymbol = input("Would you like to add this symbol (Y/n)?: ").upper()
                    if (addSymbol == "YES" or addSymbol == "Y"):
                        self.Selection()
                    elif (addSymbol == "NO" or addSymbol == "N"):
                        self.StatOptions()
                    else:
                        print("Invalid response.")
                        continue

        #if (option == 'A' or option == "CURRENT PRICE"):
            
    def TargetPrice(self, symbol): 
        if (symbol in self.stocks): 
            print(self.stocks[symbol]["1 Year Target Price"])
        else:
            print("Symbol not in database.")    
            while (1):
                addSymbol = input("Would you like to save " + symbol.upper() + "? (Y/n)").upper()
                if (addSymbol == "YES" or addSymbol == "Y"):
                    pass        #  restart here
                elif (addSymbol == "NO" or addSymbol == "N"):
                    pass        #  send to menu options
                else:
                    print("Invalid response.")
                    continue

    def Selection(self):
        '''Accepts symbols to be added to portfolio.'''
        targets = []

        print("Enter the symbols for the stock you are interested in." +
	    "\nEnter 'end' when all symbols have been input.")

        n = 0
        end = False
        while (1):
            symbol = input("Symbol " + str(n+1) + ": ").lower()
            if (symbol == "end" and len(targets) == 0):
                print("No valid symbol entered.")
                self.Redirect()
            elif (self.ValidSymbol(symbol)):   
                targets.append(symbol)
                n += 1
            else:
                continue
            
        self.StockInfo(targets, n)
        self.MainMenu()

    def StockInfo(self, targets, n):
        '''Extracts company statistics and adds data to portfolio'''
        # NASDAQ summary data is collected and stored for each valid symbol.
        labels = ["Bid/Ask", "1 Year Target Price", "---", "Share Volume", "---", "---", "52 Week High/Low", 
                    "Market Cap", "P/E", "---", "EPS", "---", "---", "---", "---", "Beta", "---", "---", 
                    "---", "---", "---"]
        for i in range(0, n):
            statistics = {}
                             
            url = "http://www.nasdaq.com/symbol/" + targets[i]
            r = requests.get(url)
                
            soup = BeautifulSoup(r.content, "html.parser")      #  html data parsed for reading

            # No unique identifiers for tds' containing summary data.
            # DOM positioning used to identify relevant data.
            table = soup.find("table", {"class": "widthF"})
            nestedTable = table.find("table")
                
            cnt = 0
            for td in nestedTable.find_all("td", {"align": "right"}):
                statistics[labels[cnt]] = re.sub('[^0-9./]', '', str(td.contents))
                cnt += 1

            del statistics["---"]

            self.stocks[targets[i]] = statistics

    def ValidSymbol(self, symbol): 
        '''Determines if symbol is a valid publicly traded company.'''
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

    def SavedSymbol(self, symbol):
        '''Determines if symbol is saved in portfolio.'''
        return symbol in self.stocks

    def Redirect(self): 
        '''Irregular selection from menus leads to redirect options.'''
        while (1):
            print("Please select from the following options:\n" + \
                "a) Continue\n" + \
                "b) Main Menu\n" + \
                "c) Quit")
            selection = input("").upper()
            if (selection == 'A' or selection == "CONTINUE"):
                return 1
            elif (selection == 'B' or selection == "MAIN MENU"):
                self.MainMenu()
            elif (selection == 'C' or selection == "QUIT"): 
                print("Program terminated.")
                sys.exit(0)
            else:
                print("Invalid option.")
                continue
