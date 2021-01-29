# Author: Tom Oter
#
# Program for finding the highest Dividend Yield 
# 


import yfinance as yf
import pandas as pd
import yaml
import logging
import logging.config

from datapackage import Package




def get_sp500(url):
    # url = https://datahub.io/core/s-and-p-500-companies#python
    logger.info(f"Getting data from {url}")
    package = Package(url)
    # print processed tabular data (if exists any)
    for resource in package.resources:
        if resource.descriptor['datahub']['type'] == 'derived/csv':
            market_list = resource.read()
    return market_list


def get_stock_symbol(market_list, index):
    return market_list[index][0]


def get_stock_symbol_list(market_list):
    return [item[0] for item in market_list]


def get_company_info(stock_symbol):
    try:
        company = yf.Ticker(stock_symbol)
        return company.info
    except Exception as e:
        logger.warning(e)
        return -1


def _split_list_by_stock_symbol(stock_symbol_list, stock_symbol):
    split_index = stock_symbol_list.index(stock_symbol)
    front_list = stock_symbol_list[:split_index]
    back_list = stock_symbol_list[split_index:]
    return (front_list, back_list)

def find_highest_DividendYield(stock_symbol_list):
    last_highest_DY           = 0
    last_highest_index        = 0
    last_highest_sym          = ""
    last_highest_company_info = {}
    index                     = 0
    DY                        = 0

    for stock_symbol in stock_symbol_list:
        logger.info(f"Evaluating: {stock_symbol}")
        company_info = get_company_info(stock_symbol)
        if company_info is not -1:
            DY = company_info['dividendYield']
            try:
                if DY is not None and DY > last_highest_DY:
                    logger.info(f"New company with top DY: {stock_symbol}")
                    last_highest_DY           = DY
                    last_highest_index        = index
                    last_highest_sym          = stock_symbol
                    last_highest_company_info = company_info
            except Exception as e:
                logger.warning(e)
            index += 1
        else:
            continue
    print(last_highest_sym)

    highest_company_params = [last_highest_DY, last_highest_index,\
                              last_highest_sym, last_highest_company_info]
    return highest_company_params    


def full_scan(stock_symbol_list):
    find_highest_DividendYield(stock_symbol_list)

def partial_scan(stock_symbol_list, stock_symbol):
    front_list, back_list = _split_list_by_stock_symbol(stock_symbol_list, stock_symbol)
    find_highest_DividendYield(back_list)    

def print_company_info(stock_symbol):
    info = get_company_info(stock_symbol)
    if info != -1:
        print(info)
    else:
        print("No info found")

def print_market_list(market_list):
    print(market_list)

def print_stock_symbol_list(stock_symbol_list):
    print(stock_symbol_list)


def event_handler(com, market_list, stock_symbol_list):
    if com == "exit":
        return False

    elif com == "full":
        print("\n")
        print("#########################")
        print("#        FULL           #")
        print("#########################\n")
        full_scan(stock_symbol_list)
        return True

    elif com == "partial":
        print("\n")
        print("#########################")
        print("#        PARTIAL        #")
        print("#########################\n")
        print("Input the company symbol")
        stock_symbol = input("> ").upper()
        partial_scan(stock_symbol_list, stock_symbol)
        return True

    elif com == "company":
        print("\n")
        print("#########################")
        print("#        COMPANY        #")
        print("#########################\n")
        print("Input the company symbol")
        stock_symbol = input("> ").upper()
        print_company_info(stock_symbol)
        return True

    elif com == "market":
        print("\n")
        print("#########################")
        print("#        MARKET         #")
        print("#########################\n")
        print_market_list(market_list)
        return True

    elif com == "symbol":
        print("\n")
        print("#########################")
        print("#        SYMBOL         #")
        print("#########################\n")
        print_stock_symbol_list(stock_symbol_list)
        return True

    else:
        print("\n")
        print("#########################")
        print("#        HELP           #")
        print("#########################\n")
        print("\t1. exit\n\t2. full\n\t3. partial\n\t4. company\n\t5. market\n\t6. symbol")
        return True



def main():
    url = 'https://datahub.io/core/s-and-p-500-companies/datapackage.json'
    market_list = get_sp500(url)
    stock_symbol_list = get_stock_symbol_list(market_list)
    
    run = True  
    while(run):
        print("\n")
        print("#########################")
        print("#        COMMAND        #")
        print("#########################\n")
        com = input("> ")
        run = event_handler(com, market_list, stock_symbol_list)



if __name__ == '__main__':
    # Setting up logger
    with open('logger.yaml', 'r') as f:
        log_cfg = yaml.safe_load(f.read())
    logging.config.dictConfig(log_cfg)
    logger = logging.getLogger(__name__)


    try:
        main()
    except KeyboardInterrupt:
        logger.info("Closing")
        exit()