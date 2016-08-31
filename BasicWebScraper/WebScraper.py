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
                self.DataDisplay()
            elif (selection == 'B' or selection == "ADD SYMBOLS TO PORTFOLIO"):
                self.AddSymbol()
            elif (selection == 'C' or selection == "QUIT"): 
                print("Program terminated.")
                sys.exit(0)
            else:
                print("Invalid option.")
                continue
    
    def DataDisplay(self): 
        choice = ""

        while (1):
            print("Display Options\n" + \
                "a) Select Symbols to Display\n" + \
                "b) Display Entire Portfolio\n" + \
                "c) Main Menu\n")

            selection = input("Please select an option: ").upper()
            choice = selection
            print("")
            if (selection == 'A' or selection == "SELECT SYMBOLS TO DISPLAY"):
                break
            elif (selection == 'B' or selection == "DISPLAY ENTIRE PORTFOLIO"):
                break 
            elif (selection == 'C' or selection == "MAIN MENU"): 
                self.MainMenu()
            else:
                print("Invalid option.")
                continue

        if (choice == 'B'):
            symbols = list(self.stocks.keys())
            bidAskList, targetList, highLowList, capList, peList, epsList, betaList = ([] for i in range(7))
            for company in self.stocks:
                bid, ask = self.stocks[company]["Bid/Ask"].split('/')
                bid = "{:.2f}".format(float(bid))
                ask = "{:.2f}".format(float(ask))
                bidAsk = bid+'/'+ask
                bidAskList.append(bidAsk)

                target = "{:.2f}".format(float(self.stocks[company]["1 Year Target Price"]))
                targetList.append(target)
                
                high, low = self.stocks[company]["52 Week High/Low"].split('/')                
                high = "{:.2f}".format(float(high))
                low = "{:.2f}".format(float(low))
                highLow = high+'/'+low
                highLowList.append(highLow)
                
                capital = "{:.2f}".format(float(self.stocks[company]["Market Cap"]))
                capList.append(capital)
                
                pe = "{:.2f}".format(float(self.stocks[company]["P/E"]))
                peList.append(pe)
                
                eps = "{:.2f}".format(float(self.stocks[company]["EPS"]))
                epsList.append(eps)
                
                beta = "{:.2f}".format(float(self.stocks[company]["Beta"]))
                betaList.append(beta)

            for sym in symbols: 
                print(sym, end="") 
                self.AlignTable(sym)
            self.AlignTable("", True, len(symbols))

            for i in range(0, len(bidAskList) // len(symbols)):
                for j in range(0, len(symbols)):
                    print(bidAskList[i+j], end ="")
                    self.AlignTable(bidAskList[i+j])
                print("")                
                for j in range(0, len(symbols)):
                    print(targetList[i+j], end ="")
                    self.AlignTable(targetList[i+j])
                print("")
                for j in range(0, len(symbols)):
                    print(highLowList[i+j], end ="")
                    self.AlignTable(highLowList[i+j])
                print("")
                for j in range(0, len(symbols)):
                    print(capList[i+j], end ='')
                    self.AlignTable(capList[i+j])
                print("")
                for j in range(0, len(symbols)):
                    print(peList[i+j], end ="")
                    self.AlignTable(peList[i+j])
                print("")
                for j in range(0, len(symbols)):
                    print(epsList[i+j], end ="")
                    self.AlignTable(epsList[i+j])
                print("")
                for j in range(0, len(symbols)):
                    print(betaList[i+j], end ="")
                    self.AlignTable(betaList[i+j])
                print("")
            print("")


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
                        self.AddSymbol()
                    elif (addSymbol == "NO" or addSymbol == "N"):
                        self.StatOptions()
                    else:
                        print("Invalid response.")
                        continue

        if (option == 'A' or option == "CURRENT PRICE"):
            self.CurrentPrice(self, targets)

            
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

    def AddSymbol(self):
        '''Accepts symbols to be added to portfolio.'''
        targets = []

        print("Enter the symbols for the stock you are interested in." +
	    "\nEnter 'end' when all symbols have been input.")

        n = 0
        end = False
        while (1):
            symbol = input("Symbol " + str(n+1) + ": ").lower()
            if (symbol == "end"):
                if (len(targets) == 0):
                    print("No valid symbol entered.")
                    self.Redirect()
                else: 
                    break
            elif (self.ValidSymbol(symbol)):   
                targets.append(symbol)
                n += 1
            else:
                continue
            
        self.StockInfo(targets, n)
        print("")
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
    
    def AlignTable(self, value, header=False, n=0):
        if (len(value) == 3): 
            print("                |", end="")
        elif (len(value) == 4):
            print("               |", end="")
        elif (len(value) == 5):
            print("              |", end="")
        elif (len(value) == 6): 
            print("             |", end="") 
        elif (len(value) == 7): 
            print("            |", end="")  
        elif (len(value) == 8):
            print("           |", end="") 
        elif (len(value) == 9): 
            print("          |", end="") 
        elif (len(value) == 10): 
            print("         |", end="")  
        elif (len(value) == 11):
            print("        |", end="") 
        elif (len(value) == 12):
            print("       |", end="") 
        elif (len(value) == 13): 
            print("      |", end="") 
        elif (len(value) == 14): 
            print("     |", end="")  
        elif (len(value) == 15):
            print("    |", end="") 

        if (header == True):
            print("")
            print("-------------------|" * n)