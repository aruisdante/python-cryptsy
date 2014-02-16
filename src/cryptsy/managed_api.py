'''
Licesnsed under the MIT License. See accompanying LICENSE.txt file for full licesnse terms.

Copyright (c) 2014 Adam Panzica

@author Adam Panzica

'''
from bare_api import general_market_data, general_orderbook_data, get_info, get_markets,\
    get_transactions, market_trades, market_orders, my_trades, my_orders, depth,\
    create_order, cancel_order, calculate_fees, generate_new_address
from datetime import datetime
from __builtin__ import dir
    
class APIError(Exception):
    '''Represents an error with an API call
    
    :type message: str
    :param message: The error message
    
    '''
    def __init__(self, message):
        super(APIError, self).__init__(message)
    
class CallResult(object):
    '''Container class for wrapping the raw data returned by an API call and detecting success or failure
    :param raw_data: Data in the form returned by any function from :mod:`cryptsy.bare_api`
    
    Can be used as a bool, where the result is the value stored in :attr:`success`
    
    '''
    def __init__(self, raw_data):
        self.success = False #: Will be True if the result in raw_data is valid
        self.data    = None  #: If success = True, this will be the data returned by the API call
        self.error   = None  #: If success = False, this will be an :class:`APIError` containing the error message
        if int(raw_data['success']) == 1:
            self.success = True
            self.data    = raw_data['return']
        else:
            self.error   = APIError(raw_data['error'])
            
    def __bool__(self):
        return self.success
    
    __nonzero__=__bool__
    
    def __str__(self):
        return 'success:{0}, error:{1}, data:{2}'.format(self.success, self.error, self.data)

class TransactionData(object):
    '''A container object for representing the data in a cryptsy transaction
    
    :param data: JSON data in the format returned by cryptsy's transaction api's (such as the dicts contained in the list returned by :func:`cryptsy.bare_api.get_transactions`)
    
    '''
    def __init__(self, data):
        try:
            self.trxid     = data['trxid']          #: Transaction ID of this transaction. For everything that is not a cryptsy points transaction, this will be a string of hex values
            self.fee       = float(data['fee'])     #: The fee from this transaction (:class:`float`)
            self.timestamp = datetime.fromtimestamp(int(data['timestamp'])) #: A :class:`~datetime.Datetime` representing when the transaction occurred
            self.datetime  = data['datetime']                               #: String representation of the value in :attr:`timestamp`
            self.currency  = data['currency']       #: The name of the source currency from this transaction
            self.amount    = float(data['amount'])  #: The amount of currency transacted (:class:`float`)
            self.address   = data['address']        #: String wallet address where the funds were deposited
            self.timezone  = data['timezone']       #: String timezone that the date values are in
            self.ttype     = data['type']           #: Will be either 'Deposit' or 'Withdrawal'
        except KeyError as e:
            raise KeyError('Mallformed Transaction Data, missing field:'+str(e))
        
    def __eq__(self, rhs):
        '''
        :return: True if self.txid == rhs.txid, or NotImplemented if rhs is not a :class:`TransactionData`
        
        '''
        if hasattr(rhs, 'trxid'):
            return self.trxid == rhs.trxid
        else:
            return NotImplemented
    
    def __ne__(self, rhs): 
        '''
        :return: True if self.txid != rhs.txid, or NotImplemented if rhs is not a :class:`TransactionData`
        
        '''
        if hasattr(rhs, 'trxid'):
            return self.trxid != rhs.trxid
        else:
            return NotImplemented
        
    def __str__(self):
        return '{{trxid:{0}, fee:{1}, timestamp:{2}, datetime:{3}, currency:{4}, amount:{5}, address:{6}, timezone:{7}, type:{8}}}'.format(self.trxid, self.fee, self.timestamp,
                                                                                                                                           self.datetime, self.currency, self.amount,
                                                                                                                                           self.address, self.timezone, self.ttype)

class ManagedAPI(object):
    '''
    
    :type application_key: str
    :param application_key: The public application key used for authenticated requests
    :type secret_key: str
    :param secret_key: The private secret key for the user for authenticated requests
    :type timeout: float
    :param timeout: Default timeout to apply to all API calls
    
    '''
    
    _last_api_call_time = None #: Used to rate-limit API calls
    
    def __init__(self, application_key, secret_key, timeout=None):
        '''
    
    
        '''
        self._application_key = application_key
        self._secret_key      = secret_key
        self.cache = {'general_market_data'    : (None, None),
                      'general_orderbook_data' : (None, None),
                      'get_info'               : (None, None),
                      'get_markets'            : (None, None),
                      'get_transactions'       : (None, None),
                      'market_trades'          : (None, None),
                      'market_orders'          : (None, None),
                      'my_trades'              : (None, None),
                      'my_orders'              : (None, None),
                      'depth'                  : (None, None),
                      'create_order'           : (None, None),
                      'cancel_order'           : (None, None),
                      'calculate_fees'         : (None, None),
                      'generate_new_address'   : (None, None),}
        self.timeout = None #: The default timeout to apply to all API calls, in seconds (:class:`float`)
        
        
    def general_market_data(self, market = None, timeout = None):
        '''
        
        
        '''
        result = CallResult(general_market_data(market, timeout))
        if result:
            return result
        else:
            raise result.error
    
    def general_orderbook_data(self, market = None, timeout = None):
        '''Gets the current state of orderbook data for either all markets or a specific market
        
        :param market: (optional) The market ID to fetch data for
        :type market: int
        :param timeout: (optional) Timeout for the request, in seconds
        :type timeout: int
        
        '''
        result = CallResult(general_orderbook_data(market, timeout))
        if result:
            return result
        else:
            raise result.error
    
    def get_info(self, timeout = None):
        '''Get's the user's account info
        
        :param application_key: The application key to apply to the API call
        :type application_key: str
        :param secret_key: The user's secret key to apply to the API call
        :type secret_key: str
        :param timeout: Timeout for the request in seconds
        
        '''
        result = CallResult(get_info(application_key = self._application_key,
                                     secret_key      = self._secret_key,
                                     timeout         = self._timeout(timeout)))
        if result:
            return result
        else:
            raise result.error
    
    def get_markets(self, timeout = None):
        '''Get's the user's active markets
        
        :param application_key: The application key to apply to the API call
        :type application_key: str
        :param secret_key: The user's secret key to apply to the API call
        :type secret_key: str
        :param timeout: Timeout for the request in seconds
        
        '''
        result = CallResult(get_markets(application_key = self._application_key,
                                        secret_key      = self._secret_key,
                                        timeout         = self._timeout(timeout)))
        if result:
            return result
        else:
            raise result.error
    
    def get_transactions(self, timeout = None):
        '''Get's the user's Deposit/Withdrawal history
        
        :param timeout: Timeout for the request in seconds
        :rtype: [:class:`TransactionData`, ...]
        :return: A list of all of the user's previous transactions
        
        '''
        result = CallResult(get_transactions(application_key = self._application_key,
                                             secret_key      = self._secret_key,
                                             timeout         = self._timeout(timeout)))
        if result:
            return [TransactionData(entry) for entry in result.data]
        else:
            raise result.error
    
    def market_trades(self, market, timeout = None):
        '''Get's the the last 1000 transactions for a market
        
        :param market: The market ID to query
        :type market: int
        :param application_key: The application key to apply to the API call
        :type application_key: str
        :param secret_key: The user's secret key to apply to the API call
        :type secret_key: str
        :param timeout: Timeout for the request in seconds
        
        '''
        result = CallResult(market_trades(application_key = self._application_key,
                                          secret_key      = self._secret_key,
                                          market          = market,
                                          timeout         = self._timeout(timeout)))
        if result:
            return result
        else:
            raise result.error
    
    def market_orders(self, market, timeout = None):
        '''Get's the the set of buy/sell orders for a market
        
        :param market: The market ID to query
        :type market: int
        :param application_key: The application key to apply to the API call
        :type application_key: str
        :param secret_key: The user's secret key to apply to the API call
        :type secret_key: str
        :param timeout: Timeout for the request in seconds
        
        '''
        result = CallResult(market_orders(application_key = self._application_key,
                                          secret_key      = self._secret_key,
                                          market          = market,
                                          timeout         = self._timeout(timeout)))
        if result:
            return result
        else:
            raise result.error
    
    def my_trades(self, market = None, limit = 200, timeout = None):
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
        result = CallResult(my_trades(application_key = self._application_key,
                                      secret_key      = self._secret_key,
                                      market          = market,
                                      limit           = limit,
                                      timeout         = self._timeout(timeout)))
        if result:
            return result
        else:
            raise result.error
    
    def my_orders(self, market = None, timeout = None):
        '''Get's the the user's current open buy/sell orders, optionally limited to a a market
        
        :param market: (optional) The market ID to query
        :type market: int
        :param application_key: The application key to apply to the API call
        :type application_key: str
        :param secret_key: The user's secret key to apply to the API call
        :type secret_key: str
        :param timeout: Timeout for the request in seconds
        
        '''
        result = CallResult(my_orders(application_key = self._application_key,
                                      secret_key      = self._secret_key,
                                      market          = market,
                                      timeout         = self._timeout(timeout)))
        if result:
            return result
        else:
            raise result.error
    
    def depth(self, market, timeout = None):
        '''Get's an array of buy and sell orders on the market representing market depth
        
        :param market: The market ID to query
        :type market: int
        :param application_key: The application key to apply to the API call
        :type application_key: str
        :param secret_key: The user's secret key to apply to the API call
        :type secret_key: str
        :param timeout: Timeout for the request in seconds
        
        '''
        result = CallResult(depth(application_key = self._application_key,
                                  secret_key      = self._secret_key,
                                  market          = market,
                                  timeout         = self._timeout(timeout)))
        if result:
            return result
        else:
            raise result.error
    
    def create_order(self, market, ordertype,  quantity, price, timeout = None):
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
        result = CallResult(create_order(application_key = self._application_key,
                                         secret_key      = self._secret_key,
                                         market          = market,
                                         ordertype       = ordertype,
                                         quantity        = quantity,
                                         price           = price,
                                         timeout         = self._timeout(timeout)))
        if result:
            return result
        else:
            raise result.error
    
    def cancel_order(self, orderid = None, market = None, timeout = None):
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
        result = CallResult(cancel_order(application_key = self._application_key,
                                         secret_key      = self._application_key,
                                         orderid         = orderid,
                                         market          = market,
                                         timeout         = self._timeout(timeout)))
        if result:
            return result
        else:
            raise result.error
    
    def calculate_fees(self, ordertype,  quantity, price, timeout = None):
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
        result = CallResult(calculate_fees(application_key = self._application_key,
                                           secret_key      = self._secret_key,
                                           ordertype       = ordertype,
                                           quantity        = quantity,
                                           price           = price,
                                           timeout         = self._timeout(timeout)))
        if result:
            return result
        else:
            raise result.error
    
    def generate_new_address(self, currencycode = None, currencyid = None, timeout = None):
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
        result = CallResult(generate_new_address(application_key = self._application_key,
                                                 secret_key      = self._secret_key,
                                                 currencycode    = currencycode,
                                                 currencyid      = currencycode,
                                                 timeout         = self._timeout(timeout)))
        if result:
            return result
        else:
            raise result.error
        
    def _timeout(self, timeout):
        '''
        :type timeout: float
        :param timeout: timeout in seconds or None
        :rtype: float
        :return: timeout if timeout!=None, else :attr:`timeout`
        
        '''
        if timeout:
            return timeout
        else:
            return self.timeout
    
    
    