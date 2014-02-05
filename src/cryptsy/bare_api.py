'''
.. module:: bare_api
   :platform: Linux, Windows, OSX
   :synopsis: A set of methods for accessing the Cryptsy API
..  moduleauthor:: Adam Panzica

Licesnsed under the MIT License. See accompanying LICENSE.txt file for full licesnse terms.
Copyright (c) 2014 Adam Panzica
   
'''
import urllib, urllib2, json, hashlib, hmac
import time

__PUB_API_BASE__ = 'http://pubapi.cryptsy.com/api.php?'
__PRI_API_BASE__ = 'https://api.cryptsy.com/api'

def call_pub_api(method, inputs, timeout = None):
    '''Calls a public API method
    
    :param method: The method to call
    :type method: str
    :param inputs: An array of tuples in the form (key,value) for input values
    :type inputs: [(str,stringable),...]
    :param timeout: Timeout for the request in seconds
    :type timeout: float
    :return: file-like -- A json encoded object with the results of the API call
    
    '''
    inputs.append(('method', method))
    api_call = urllib2.urlopen(url =  __PUB_API_BASE__, data = urllib.urlencode(inputs), timeout = timeout)
    return json.load(api_call)

def call_pri_api(method, inputs, application_key, secret_key, timeout = None):
    '''Calls a private API method
    
    :param method: The method to call
    :type method: str
    :param inputs: An array of tuples in the form (key,value) for input values
    :type inputs: [(str,stringable),...]
    :param application_key: The application key to apply to the API call
    :type application_key: str
    :param secret_key: The user's secret key to apply to the API call
    :type secret_key: str
    :param timeout: Timeout for the request in seconds
    :type timeout: float
    :return: file-like -- A json encoded object with the results of the API call
    
    '''
    inputs.append(('method', method))
    inputs.append(('nonce', int(time.time())))
    signable   = urllib.urlencode(inputs)
    sign       = hmac.new(secret_key, signable, hashlib.sha512).hexdigest()
    headers    = {'Key':application_key, 'Sign':sign}
    api_call = urllib2.urlopen(urllib2.Request(__PRI_API_BASE__, signable, headers), timeout=timeout)
    return json.load(api_call)

def general_market_data(market = None, timeout = None):
    '''Gets the current state of market data for either all markets or a specific market
    
    :param market: (optional) The market ID to fetch data for
    :type market: int
    :param timeout: (optional) Timeout for the request, in seconds
    :type timeout: int
    
    '''
    if market:
        method = 'singlemarketdata'
        inputs = [('marketid', market)]
    else:
        method = 'marketdatav2'
        inputs = []
    data = call_pub_api(method, inputs, timeout)
    return data

def general_orderbook_data(market = None, timeout = None):
    '''Gets the current state of orderbook data for either all markets or a specific market
    
    :param market: (optional) The market ID to fetch data for
    :type market: int
    :param timeout: (optional) Timeout for the request, in seconds
    :type timeout: int
    
    '''
    if market:
        method = 'singleorderdata'
        inputs = [('marketid', market)]
    else:
        method = 'orderdata'
        inputs = []
    data = call_pub_api(method, inputs, timeout)
    return data

def get_info(application_key, secret_key, timeout = None):
    '''Get's the user's account info
    
    :param application_key: The application key to apply to the API call
    :type application_key: str
    :param secret_key: The user's secret key to apply to the API call
    :type secret_key: str
    :param timeout: Timeout for the request in seconds
    
    '''
    data = call_pri_api('getinfo', [], application_key, secret_key, timeout)
    return data

def get_markets(application_key, secret_key, timeout = None):
    '''Get's the user's active markets
    
    :param application_key: The application key to apply to the API call
    :type application_key: str
    :param secret_key: The user's secret key to apply to the API call
    :type secret_key: str
    :param timeout: Timeout for the request in seconds
    
    '''
    data = call_pri_api('getmarkets', [], application_key, secret_key, timeout)
    return data

def get_transactions(application_key, secret_key, timeout = None):
    '''Get's the user's Deposit/Withdrawal history
    
    :param application_key: The application key to apply to the API call
    :type application_key: str
    :param secret_key: The user's secret key to apply to the API call
    :type secret_key: str
    :param timeout: Timeout for the request in seconds
    
    '''
    data = call_pri_api('mytransactions', [], application_key, secret_key, timeout)
    return data

def market_trades(application_key, secret_key, market, timeout = None):
    '''Get's the the last 1000 transactions for a market
    
    :param market: The market ID to query
    :type market: int
    :param application_key: The application key to apply to the API call
    :type application_key: str
    :param secret_key: The user's secret key to apply to the API call
    :type secret_key: str
    :param timeout: Timeout for the request in seconds
    
    '''
    data = call_pri_api('markettrades', [], application_key, secret_key, timeout)
    return data

def market_orders(application_key, secret_key, market, timeout = None):
    '''Get's the the set of buy/sell orders for a market
    
    :param market: The market ID to query
    :type market: int
    :param application_key: The application key to apply to the API call
    :type application_key: str
    :param secret_key: The user's secret key to apply to the API call
    :type secret_key: str
    :param timeout: Timeout for the request in seconds
    
    '''
    data = call_pri_api('marketorders', [('marketid',market)], application_key, secret_key, timeout)
    return data 

def my_trades(application_key, secret_key, market = None, limit = 200, timeout = None):
    '''Get's the the trade history for the user, optionally limited to a given market
    
    :param market: (optional) The market ID to query
    :type market: int
    :param application_key: The application key to apply to the API call
    :type application_key: str
    :param secret_key: The user's secret key to apply to the API call
    :type secret_key: str
    :param limit: (optional) The maximum number of transactions to list. Ignored if market is not specified
    :type limit: int
    :param timeout: Timeout for the request in seconds
    
    '''
    if market:
        method = 'marketorders'
        inputs = [('marketid',market), ('limit',market)]
    else:
        method = 'allmytrades'
        inputs = []
    data = call_pri_api(method, inputs, application_key, secret_key, timeout)
    return data

def my_orders(application_key, secret_key, market = None, timeout = None):
    '''Get's the the user's current open buy/sell orders, optionally limited to a a market
    
    :param market: (optional) The market ID to query
    :type market: int
    :param application_key: The application key to apply to the API call
    :type application_key: str
    :param secret_key: The user's secret key to apply to the API call
    :type secret_key: str
    :param timeout: Timeout for the request in seconds
    
    '''
    if market:
        method = 'myorders'
        inputs = [('marketid',market)]
    else:
        method = 'allmyorders'
        inputs = []
    data = call_pri_api(method, inputs, application_key, secret_key, timeout)
    return data 

def depth(application_key, secret_key, market, timeout = None):
    '''Get's an array of buy and sell orders on the market representing market depth
    
    :param market: The market ID to query
    :type market: int
    :param application_key: The application key to apply to the API call
    :type application_key: str
    :param secret_key: The user's secret key to apply to the API call
    :type secret_key: str
    :param timeout: Timeout for the request in seconds
    
    '''
    data = call_pri_api('depth', [('marketid',market)], application_key, secret_key, timeout)
    return data 

def create_order(application_key, secret_key, market, ordertype,  quantity, price, timeout = None):
    '''Creates an order on a market
    
    :param market: The market ID to query
    :type market: int
    :param ordertype: Buy|Sell
    :type ordertype: str
    :param quantity: The amount of units to buy/sell
    :type quantity: float
    :param price: The price to buy/sell at
    :type price: float
    :param application_key: The application key to apply to the API call
    :type application_key: str
    :param secret_key: The user's secret key to apply to the API call
    :type secret_key: str
    :param timeout: Timeout for the request in seconds
    
    '''
    data = call_pri_api('createorder', [('marketid',market), ('ordertype',ordertype), ('quantity',quantity), ('price',price)], application_key, secret_key, timeout)
    return data

def cancel_order(application_key, secret_key, orderid = None, market = None, timeout = None):
    '''Cancels an order, all orders on a market, or all orders across all markets
    
    :param orderid: (optional) The order to cancel
    :param orderid: int
    :param market: (optional) The market to cancel orders for
    :type market: int
    :param application_key: The application key to apply to the API call
    :type application_key: str
    :param secret_key: The user's secret key to apply to the API call
    :type secret_key: str
    :param timeout: Timeout for the request in seconds
    
    If an order id is given, cancels just that order. If a market id is given (but not an order ID), cancels all orders on that market.
    If neither an order id or market id are given, cancels all open orders for the user
    
    '''
    if orderid:
        method = 'cancelorder'
        inputs = [('orderid', orderid)]
    elif market:
        method = 'cancelmarketorders'
        inputs = [('marketid', market)] 
    else:
        method = 'cancelallorders'       
        inputs = []
    data = call_pri_api(method, inputs, application_key, secret_key, timeout)
    return data 

def calculate_fees(application_key, secret_key, ordertype,  quantity, price, timeout = None):
    '''Calculates the fees that would be assessed for an order
    
    :param ordertype: Buy|Sell
    :type ordertype: str
    :param quantity: The amount of units to buy/sell
    :type quantity: float
    :param price: The price to buy/sell at
    :type price: float
    :param application_key: The application key to apply to the API call
    :type application_key: str
    :param secret_key: The user's secret key to apply to the API call
    :type secret_key: str
    :param timeout: Timeout for the request in seconds
    
    '''
    data = call_pri_api('calculatefees', [('ordertype',ordertype), ('quantity',quantity), ('price',price)], application_key, secret_key, timeout)
    return data

def generate_new_address(application_key, secret_key, currencycode = None, currencyid = None, timeout = None):
    '''Creates a new deposite address for the specified currency.
    
    :param currencycode: The currency code to create an address for (EX: 'BTC' = Bitcoin)
    :param currencycode: str
    :param currencyid: The currency id to create an address for (EX: 3 = Bitcoin)
    :type currencyid: int
    :param application_key: The application key to apply to the API call
    :type application_key: str
    :param secret_key: The user's secret key to apply to the API call
    :type secret_key: str
    :param timeout: Timeout for the request in seconds
    
    Only need to specify currency code OR currency id, not both
    
    '''
    method = 'generatenewadress'
    if currencycode:
        inputs = [('currencycode', currencycode)]
    elif currencyid:
        inputs = [('currencyid', currencyid)]
    else:
        inputs = []
    data = call_pri_api(method, inputs, application_key, secret_key, timeout)
    return data  