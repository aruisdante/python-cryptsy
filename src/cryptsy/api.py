'''
Licesnsed under the MIT License. See accompanying LICENSE.txt file for full licesnse terms.

Copyright (c) 2014 Adam Panzica

@author Adam Panzica

'''
import urllib, urllib2, json, hashlib, hmac
import time

__PUB_API_BASE__ = 'http://pubapi.cryptsy.com/api.php?'
__PRI_API_BASE__ = 'https://api.cryptsy.com/api'

def call_pub_api(method, inputs, timeout = None):
    '''
    Calls a public API method
    :param method: The method to call
    :type method: str
    :param inputs: An array of tuples in the form (key,value) for input values
    :type inputs: [(str,stringable),...]
    :param timeout: Timeout for the request in seconds
    :type timeout: float
    :return file-like -- A json encoded object with the results of the API call
    
    '''
    inputs.append(('method', method))
    api_call = urllib2.urlopen(url =  __PUB_API_BASE__, data = urllib.urlencode(inputs), timeout = timeout)
    return json.load(api_call)

def call_pri_api(method, inputs, application_key, secret_key, timeout = None):
    '''
    Calls a private API method
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
    :return file-like -- A json encoded object with the results of the API call
    
    '''
    inputs.append(('method', method))
    inputs.append(('nonce', int(time.time())))
    sign       = hmac.new(secret_key, urllib.urlencode(inputs), hashlib.sha512).hexdigest()
    headers    = {'Key':application_key, 'Sign':sign}
    api_call = urllib2.urlopen(urllib2.Request(__PRI_API_BASE__, urllib.urlencode(inputs), headers), timeout=timeout)
    return json.load(api_call)

def general_market_data(market = None, timeout = None):
    '''
    Gets the current state of market data for either all markets or a specific market
    :param market: (optional) The market ID to fetch data for
    :type market: int
    :param timeout: (optional) Timeout for the request, in seconds
    :type timeout: int
    
    '''
    data = None
    if market:
        data = call_pub_api('singlemarketdata', [('marketid', market)], timeout)
    else:
        data = call_pub_api('marketdatav2', [], timeout)
    return data

def general_orderbook_data(market = None, timeout = None):
    '''
    Gets the current state of orderbook data for either all markets or a specific market
    :param market: (optional) The market ID to fetch data for
    :type market: int
    :param timeout: (optional) Timeout for the request, in seconds
    :type timeout: int
    
    '''
    data = None
    if market:
        data = call_pub_api('singleorderdata', [('marketid', market)], timeout)
    else:
        data = call_pub_api('orderdata', [], timeout)
    return data

def get_info(application_key, secret_key, timeout = None):
    '''
    Get's the user's account info
    :param application_key: The application key to apply to the API call
    :type application_key: str
    :param secret_key: The user's secret key to apply to the API call
    :type secret_key: str
    :param timeout: Timeout for the request in seconds
    
    '''
    data = call_pri_api('getinfo', [], application_key, secret_key, timeout)
    return data

def get_markets(application_key, secret_key, timeout = None):
    '''
    Get's the user's active markets
    :param application_key: The application key to apply to the API call
    :type application_key: str
    :param secret_key: The user's secret key to apply to the API call
    :type secret_key: str
    :param timeout: Timeout for the request in seconds
    
    '''
    data = call_pri_api('getmarkets', [], application_key, secret_key, timeout)
    return data

def get_transactions(application_key, secret_key, timeout = None):
    '''
    Get's the user's Deposit/Withdrawal history
    :param application_key: The application key to apply to the API call
    :type application_key: str
    :param secret_key: The user's secret key to apply to the API call
    :type secret_key: str
    :param timeout: Timeout for the request in seconds
    
    '''
    data = call_pri_api('mytransactions', [], application_key, secret_key, timeout)
    return data

def market_trades(market, application_key, secret_key, timeout = None):
    '''
    Get's the the last 1000 transactions for a market
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

def market_orders(market, application_key, secret_key, timeout = None):
    '''
    Get's the the set of buy/sell orders for a market
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

def my_trades(market = None, application_key, secret_key, limit = 200, timeout = None):
    '''
    Get's the the trade history for the user, optionally limited to a given market
    :param market: (optional) The market ID to query
    :type market: int
    :param application_key: The application key to apply to the API call
    :type application_key: str
    :param secret_key: The user's secret key to apply to the API call
    :type secret_key: str
    :param limit: The maximum number of transactions to list
    :type limit: int
    :param timeout: Timeout for the request in seconds
    
    '''
    data = None
    if market:
        data = call_pri_api('marketorders', [('marketid',market), ('limit',market)], application_key, secret_key, timeout)
    else:
        data = call_pri_api('allmytrades', [], application_key, secret_key, timeout)
    return data

def my_orders(market = None, application_key, secret_key, timeout = None):
    '''
    Get's the the user's current open buy/sell orders, optionally limited to a a market
    :param market: (optional) The market ID to query
    :type market: int
    :param application_key: The application key to apply to the API call
    :type application_key: str
    :param secret_key: The user's secret key to apply to the API call
    :type secret_key: str
    :param timeout: Timeout for the request in seconds
    
    '''
    data = None
    if market:
        data = call_pri_api('myorders', [('marketid',market)], application_key, secret_key, timeout)
    else:
        data = call_pri_api('allmyorders', [], application_key, secret_key, timeout)
    return data 

def depth(market, application_key, secret_key, timeout = None):
    '''
    Get's an array of buy and sell orders on the market representing market depth
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



