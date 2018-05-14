#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

from pprintpp import pprint
import copy
import sys
import getopt
import queue
import datetime as dt
import hashlib
from pymemcache.client import base
import ujson as json
import requests

import pandas as pd
pd.set_option('display.float_format', lambda x: '%.4f' % x)

import logging
from concurrent import futures
from urllib.parse import unquote as urldecode

### The following is my own code libraries shared on Pypi for Logging.
from logging_fortified import (get_logger, LoggingFormat, LoggingOutput)
from requests_fortified.errors import (
    get_exception_message,
)

### The following is my own code libraries shared on Pypi for Requests.
from requests_fortified.support import (
    base_class_name,
    HEADER_CONTENT_TYPE_APP_JSON,)
from requests_fortified import RequestsFortifiedDownload

try:
    from support.month_day_range import month_day_range
except ImportError:
    from .support.month_day_range import month_day_range
try:
    from support.month_list import month_list
except ImportError:
    from .support.month_list import month_list
try:
    from errors.errors_traceback import print_traceback
except ImportError:
    from .errors.errors_traceback import print_traceback

SECONDS_FOR_60_MINUTES = 3600

class StockInvestorTask(object):
    """ENUM
    """
    UNDEFINED = None
    AVERAGE_MONTHLY_OPEN_CLOSE = "avg-monthly"
    MAX_DAILY_PROFIT = "max-daily-profit"
    BUSY_DAY = "busy-day"
    BIGGEST_LOSER = "biggest-loser"


class StockCache(object):
    """StockCache
    With the expectation the external handling of caching needs will be `memcached`.
    """

    @property
    def cache_client(self):
        return self.__cache_client
    @cache_client.setter
    def cache_client(self, value):
        self.__cache_client = value

    def __init__(self):
        # Run `memcached` before running this next line:
        self.cache_client = base.Client(('localhost', 11211))

    @staticmethod
    def cache_value_serialize(cache_value):
        try:
            if isinstance(cache_value, dict):
                external_cache_value = json.dumps(cache_value, double_precision=4, sort_keys=True)
            elif isinstance(cache_value, list):
                external_cache_value = json.dumps(cache_value, double_precision=4)
            else:
                external_cache_value = cache_value
        except TypeError:
            raise
        except Exception:
            raise

        return external_cache_value

    @staticmethod
    def cache_value_deserialize(cache_value):
        try:
            cache_value = json.loads(cache_value)
        except ValueError as json_decode_ex:
            if isinstance(cache_value, str):
                cache_value = cache_value
            elif isinstance(cache_value, bytes):
                cache_value = cache_value.decode("utf-8")
            else:
                raise Exception(
                    error_message=get_exception_message(json_decode_ex),
                    errors=json_decode_ex
                )
        except Exception:
            raise

        return cache_value


class StockInvestorTaskBase(object):
    """StockInvestorTaskBase
    Base handler of content for processed Tasks
    """
    def __init__(self, security, start_date, end_date):
        self.__stock = security
        self.__start_date = start_date
        self.__end_date = end_date

    @property
    def stock(self):
        return self.__stock
    @property
    def start_date(self):
        return self.__start_date
    @property
    def end_date(self):
        return self.__end_date

    @property
    def str(self):
        return "{}: '{}' - '{}'".format(
            self.stock,
            self.start_date,
            self.end_date
        )

    @property
    def cache_data_key(self):
        return self.cache_key("data")

    @property
    def cache_columns_key(self):
        return self.cache_key("columns")

    def cache_key(self, salt):
        cache_key_tag = "{}{}{}{}".format(
            self.stock,
            self.start_date,
            self.end_date,
            salt
        ).encode('utf-8')
        return str(int(hashlib.md5(cache_key_tag).hexdigest(), 16))


class StockInvestorRequest(StockInvestorTaskBase):
    """StockInvestorRequest
    Base handler of content for processed Task requests.
    """
    def __init__(self, stock, start_date, end_date):
        super(StockInvestorRequest, self).__init__(stock, start_date, end_date)


class StockInvestorResponse(StockInvestorTaskBase):
    """StockInvestorResponse
    Base handler of content for processed Task responses.
    """
    def __init__(self, stock, start_date, end_date, columns, data):
        super(StockInvestorResponse, self).__init__(stock, start_date, end_date)
        self.__columns = columns
        self.__data = data

    @property
    def columns(self):
        return self.__columns
    @property
    def data(self):
        return self.__data

    @property
    def str(self):
        return "{}: '{}' - '{}', {}, {}".format(
            self.stock,
            self.start_date,
            self.end_date,
            self.columns,
            len(self.data)
        )

    def serialize(self):
        return {"data": self.data, "columns": self.columns}


class StockInvestor(object):
    """Core class of this application. Provided a data range and a set of Stock symbols,
        split requests by month and by stock, handle requests to WIKI API in
        a multithreaded asynchronous manner.
    """
    __NAME = "Stock Investor"
    __VERSION = "0.0.1"

    _URL_QUANDL_WIKI_TMPL = "https://www.quandl.com/api/v3/datasets/WIKI/{0}/data.json"

    _MAX_WORKERS = 10

    @property
    def worker_queue(self):
        return self.__worker_queue
    @worker_queue.setter
    def worker_queue(self, value):
        self.__worker_queue = value

    @property
    def df(self):
        return self.__df
    @df.setter
    def df(self, value):
        self.__df = value

    @property
    def start_datetime(self):
        return self.__start_date
    @start_datetime.setter
    def start_datetime(self, value):
        self.__start_date = value

    @property
    def end_datetime(self):
        return self.__end_date
    @end_datetime.setter
    def end_datetime(self, value):
        self.__end_date = value

    @property
    def task(self):
        return self.__task
    @task.setter
    def task(self, value):
        self.__task = value

    @property
    def cache(self):
        return self.__cache.cache_client
    @cache.setter
    def cache(self, value):
        self.__cache = value

    @property
    def api_key(self):
        return self.__api_key
    @api_key.setter
    def api_key(self, value):
        self.__api_key = value

    @property
    def stocks_data(self):
        return self.__stocks_data
    @stocks_data.setter
    def stocks_data(self, value):
        self.__stocks_data = value

    #
    # Initialize
    #
    def __init__(self, kv):
        """Initialize
        """
        self.worker_queue = queue.Queue()
        self.verbose = kv.get("verbose", False)
        self.task = kv.get("task", None)
        self.api_key = kv.get("api-key", None)
        self.start_datetime = kv.get("start-datetime", None)
        self.end_datetime = kv.get("end-datetime", None)
        self.stocks = kv.get("stocks", None)

        assert self.api_key
        assert self.start_datetime
        assert self.end_datetime
        assert self.stocks

        self.cache = StockCache()

        self.run_start_time = dt.datetime.now()

        logger_level, logger_format, logger_output = (logging.INFO, LoggingFormat.JSON, LoggingOutput.STDOUT_COLOR)
        if self.verbose:
            logger_level = logging.DEBUG

        self.logger_level = logger_level
        self.logger_format = logger_format
        self.logger_output = logger_output

        self.logger = get_logger(
            logger_name=self.__NAME,
            logger_version=self.__VERSION,
            logger_format=self.logger_format,
            logger_level=self.logger_level,
            logger_output=self.logger_output
        )

        self.worker_queue_populate()
        self.__stocks_data = {}
        for stock in self.stocks:
            self.__stocks_data[stock] = {"columns": None, "data": []}

    __base_request = None
    @property
    def base_request(self):
        if self.__base_request is None:
            self.__base_request = RequestsFortifiedDownload(
                logger_format=self.logger_format,
                logger_level=self.logger_level,
                logger_output=self.logger_output
            )

        return self.__base_request

    def worker_queue_populate(self):
        """Take request parameters and break into separate tasks, primarily by
        stock symbol and monthly segmented stock dates.
        """
        assert self.start_datetime
        assert self.end_datetime

        months = month_list(self.start_datetime, self.end_datetime)
        for month in months:
            month_start_datetime, month_end_datetime = month_day_range(month)
            if self.start_datetime > month_start_datetime:
                month_start_datetime = self.start_datetime
            if self.end_datetime < month_end_datetime:
                month_end_datetime = self.end_datetime
            for stock in self.stocks:
                worker_task = StockInvestorRequest(
                    stock=stock,
                    start_date=month_start_datetime.strftime("%Y-%m-%d"),
                    end_date=month_end_datetime.strftime("%Y-%m-%d")
                )
                self.logger.debug(worker_task)
                self.__worker_queue.put(worker_task)

    #
    # Worker:
    #
    def work(
        self
    ):
        """Multithreaded handling of a split request into multiple tasks which pulled from
        worker queue as the executor is made available.

        :return: JSON: Found Result
        """

        result = None

        try:
            num_worker_threads = self._MAX_WORKERS
            with futures.ThreadPoolExecutor(max_workers=num_worker_threads) as executor:
                # executor.submit schedule self.process_account to be executed
                # for each account and returns a future representing this
                # pending operation.
                threads = []
                while not self.__worker_queue.empty():
                    wreq = self.__worker_queue.get()

                    self.logger.debug("cache: pre-get: {}".format(wreq.str))
                    wresp_data_serialized = self.cache.get(wreq.cache_data_key)
                    wresp_columns_serialized = self.cache.get(wreq.cache_columns_key)

                    if wresp_data_serialized is not None:
                        wresp_data = StockCache.cache_value_deserialize(wresp_data_serialized)
                        wresp_columns = StockCache.cache_value_deserialize(wresp_columns_serialized)
                        self.logger.debug("cache: hit: {}".format(wreq.str))
                        self.stocks_data[wreq.stock]["data"] += wresp_data
                        self.stocks_data[wreq.stock]["columns"] = wresp_columns
                        continue

                    self.logger.debug("cache: miss: {}".format(wreq))
                    future = executor.submit(self.work_process, wreq)
                    threads.append(future)

                    for future in futures.as_completed(threads):
                        wresp = future.result()
                        if not wresp:
                            self.logger.warning("No response")
                            continue

                        self.stocks_data[wresp.stock]["columns"] = wresp.columns
                        self.stocks_data[wresp.stock]["data"] += wresp.data

                        self.logger.debug("cache: pre-set: {}".format(wresp.str))

                        wresp_data_serialized = StockCache.cache_value_serialize(wresp.data)
                        self.cache.set(wresp.cache_data_key, wresp_data_serialized)

                        wresp_columns_serialized = StockCache.cache_value_serialize(wresp.columns)
                        self.cache.set(wresp.cache_columns_key, wresp_columns_serialized)

            self.stock_dataframe()

            if self.task == StockInvestorTask.AVERAGE_MONTHLY_OPEN_CLOSE:
                result = self.task_average_monthly_open_close()
            elif self.task == StockInvestorTask.MAX_DAILY_PROFIT:
                result = self.task_max_daily_profit()
            elif self.task == StockInvestorTask.BUSY_DAY:
                result = self.task_busy_day()
            elif self.task == StockInvestorTask.BIGGEST_LOSER:
                result = self.task_biggest_loser()

        except Exception as ex:
            self.logger.error(
                'Worker: Failed: Unexpected Error',
                extra={'error_exception': base_class_name(ex),
                       'error_details': get_exception_message(ex)})
            raise

        return result

    def work_process(self, wreq):
        """Processes a single request to QUANDL WIKI API

        :param wreq: StockInvestorRequest
        :return: StockInvestorResponse
        """
        self.logger.debug("Process: {}".format(wreq))

        request_params = {
            "start_date": wreq.start_date,
            "end_date": wreq.end_date,
            "api_key": self.api_key,
            "order": "asc",
        }

        request_url = self._URL_QUANDL_WIKI_TMPL.format(wreq.stock)
        try:
            response = self.worker_request(
                request_method="GET",
                request_url=request_url,
                request_headers=HEADER_CONTENT_TYPE_APP_JSON,
                request_params=request_params
            )
        except Exception as ex:
            return None

        if response is None:
            return None

        status_code = response.status_code
        if status_code != 200:
            return None

        json_data = json.loads(response.text)

        dataset_columns = json_data['dataset_data']['column_names']
        dataset_data = json_data['dataset_data']['data']

        wresp = StockInvestorResponse(
            stock=wreq.stock,
            start_date=wreq.start_date,
            end_date=wreq.end_date,
            columns=dataset_columns,
            data=dataset_data
        )

        return wresp

    def worker_request(
        self,
        request_method,
        request_url,
        request_params=None,
        request_data=None,
        request_retry=None,
        request_headers=None,
        request_label=None
    ):
        """Wrapper to requests handler created in requests-fortified.
        :param request_method:
        :param request_url:
        :param request_params:
        :param request_data:
        :param request_retry:
        :param request_headers:
        :param request_label:
        :return:
        """
        request_data_decoded = None
        if request_data:
            request_data_decoded = urldecode(request_data)

        self.logger.debug(
            "Request",
            extra={
                'request_method': request_method,
                'request_url': request_url,
                'request_params': request_params,
                'request_data_decoded': request_data_decoded})

        response = None
        tries = 0

        while True:
            tries += 1
            if tries > 1:
                _request_label = f'{request_label}: Attempt {tries}'
            else:
                _request_label = request_label

            try:
                response = self.base_request.request(
                    request_method=request_method,
                    request_url=request_url,
                    request_params=request_params,
                    request_data=request_data,
                    request_retry=request_retry,
                    request_retry_excps_func=None,
                    request_headers=request_headers,
                    request_label=_request_label
                )
            except requests.exceptions.RetryError as ex:
                self.logger.warning(
                    "Request Error",
                    extra={
                        "request_url": request_url,
                        "error": get_exception_message(ex)
                    }
                )
                continue

            except Exception as ex:
                self.logger.error(
                    "Request Error",
                    extra={
                        "request_url": request_url,
                        "error": get_exception_message(ex)
                    }
                )
                raise

            return response

    def stock_dataframe(self):
        """Build Pandas Dataframe from cached collected data."""
        self.logger.debug("Data", extra = self.stocks_data )

        self.df = None
        for stock, stock_data in self.stocks_data.items():
            dataset_columns = ["Stock"] + stock_data["columns"]
            dataset_data = [[stock] + i for i in stock_data["data"]]

            if self.df is None:
                self.df = pd.DataFrame(columns=dataset_columns)
            stocks = json.loads(json.dumps([dict(zip(dataset_columns, i)) for i in dataset_data]))
            self.df = self.df.append(stocks, ignore_index=False)

        self.df = self.df.sort_values(by=["Stock", "Date"])

    def task_average_monthly_open_close(self):
        """Average Monthly Open and Close"""
        average_monthly_open_close = {}
        for stock in self.stocks:
            average_monthly_open_close_stock = self.task_average_monthly_open_close_by_stock(stock)
            average_monthly_open_close.update(average_monthly_open_close_stock)

        return average_monthly_open_close

    def task_average_monthly_open_close_by_stock(self, stock):
        """Average Monthly Open and Close by Stock"""
        df = self.df.copy()

        criteria_stock = (df['Stock'] == stock)
        df_stock = df.copy()[criteria_stock]

        df_stock['YearMonth'] = pd.to_datetime(df_stock['Date']).map(lambda dt: dt.strftime("%Y-%m"))
        df_mean = df_stock.groupby(['Stock', 'YearMonth'], as_index=False)['Open', 'Close'].mean()

        average_monthly_open_close = {}
        average_monthly_open_close[stock] = []

        for key, month in df_mean['YearMonth'].items():
            average_open = df_mean['Open'][key]
            average_close = df_mean['Close'][key]

            average_entry = {
                'month': month,
                'average_open': average_open,
                'average_close': average_close
            }
            average_monthly_open_close[stock] += [average_entry]

        return average_monthly_open_close

    def task_max_daily_profit(self):
        df = self.df.copy()

        df['Profit'] = df['High'] - df['Low']

        max_daily_profit = []
        for stock in self.stocks:
            max_daily_profit.append(self.task_max_daily_profit_by_stock(df, stock))

        return max_daily_profit

    def task_max_daily_profit_by_stock(self, df, stock):
        df = copy.copy(df)

        criteria_stock = (df['Stock'] == stock)
        df_stock = df.copy()[criteria_stock]

        df_slice_json = json.loads(df_stock.ix[df_stock['Profit'].idxmax()][['Stock', 'Date', 'Profit']].to_json())

        return df_slice_json

    def task_busy_day(self):
        # We’d like to know which days generated unusually high activity for our securities.
        # Please display the ticker symbol, date, and volume for each day where the volume was more than 10% higher
        # than the security’s average volume (Note: You’ll need to calculate the average volume, and should display
        # that somewhere too).

        busy_day = []
        for stock in self.stocks:
            busy_day.append(self.task_busy_day_by_stock(stock))

        return busy_day

    def task_busy_day_by_stock(self, stock):
        df = self.df.copy()

        criteria_stock = (df['Stock'] == stock)
        # criteria_row_indices = df[criteria_stock].index
        # df_stock = df.copy().loc[criteria_row_indices, :]
        df_stock = df.copy()[criteria_stock]

        df_stock['Volume Mean'] = df_stock['Volume'].mean()

        dfColumnVolumeHigh = ((df_stock['Volume'] - df_stock['Volume Mean'])/ df_stock['Volume Mean']) * 100
        df_stock['Volume High'] = dfColumnVolumeHigh
        stock_slice_VH = df_stock['Volume High'] > 10

        df_slice_json = json.loads(df_stock[stock_slice_VH][['Stock', 'Date', 'Volume', 'Volume Mean']].to_json())
        busy_day = {}
        busy_day[stock] = []

        for key, date in df_slice_json['Date'].items():
            volume = df_slice_json['Volume'][key]
            volume_mean = df_slice_json['Volume Mean'][key]

            volume_entry = {
                'date': date,
                'volume': volume,
                'volume_mean': volume_mean
            }
            busy_day[stock] += [volume_entry]

        # pprint(df_stock[['Stock', 'Date', 'Volume', 'Volume Mean', 'Volume High']])

        return busy_day

    def task_biggest_loser(self):
        biggest_losers = {}
        for stock in self.stocks:
            biggest_losers.update(self.task_biggest_loser_by_stock(stock))

        biggest_loser = None
        for vstock, vnumber_of_lose_days in biggest_losers.items():
            if not biggest_loser:
                biggest_loser = {vstock: vnumber_of_lose_days}
                continue

            stock = list(biggest_loser.keys())[0]
            number_of_lose_days = biggest_loser[stock]

            if vnumber_of_lose_days > number_of_lose_days:
                biggest_loser = {vstock: vnumber_of_lose_days}

        return biggest_loser

    def task_biggest_loser_by_stock(self, stock):
        pd.set_option('display.float_format', lambda x: '%.4f' % x)

        df = self.df.copy()
        criteria_stock = (df['Stock'] == stock)
        df_slice = df[criteria_stock]
        number_of_lose_days = df_slice[(df_slice['Close'] < df_slice['Open'])].count()[1]

        return {stock: number_of_lose_days}


def main():

    yesterday_datetime_default = dt.datetime.now() - dt.timedelta(days=1)
    yesterday_date_default = yesterday_datetime_default.strftime("%Y-%m-%d")

    stock_symbols_default = ["COF", "GOOGL", "MSFT"]

    usage = ("""Usage: {0} 
        [-v | --verbose] 
        [-h | --help] 
        --api-key='API-KEY' 
       [--stocks=Stock,Stock,Stock]
       [--start-date='YYYY-MM-DD'] 
       [--end-date='YYYY-MM-DD'] 
       [--help | --avg-monthly-open-close | --max-daily-profit | --busy-day | --biggest-loser]
    -v | --verbose: Provide verbose details
    -h | --help: Usage
    --api-key: Quandl WIKI API Key [Required]
    --start-date: 'YYYY-MM-DD' Default: '{1}'
    --end-date: 'YYYY-MM-DD' Default: '{2}'
    --stocks: List of WIKI Stock Symbols [Required] Default: {3}
    --avg-monthly: Average Monthly Open and Close prices for each stock. Default.
    --max-daily-profit: Which day provided the highest amount of profit for each stock.
    --busy-day: Which days generated unusually high activity for each stock.
    --biggest-loser: Which stock had the most days where the closing price was lower than the opening price.
    """).format(sys.argv[0], yesterday_date_default, yesterday_date_default, str(stock_symbols_default))

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hv",
            ["help", "verbose", "api-key=", "stocks=", "start-date=", "end-date=", "avg-monthly-open-close", "max-daily-profit", "busy-day", "biggest-loser"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        print(usage)
        sys.exit(1)

    kv = {}
    for opt, val in opts:
        if opt in ("-v", "--verbose"):
            kv["verbose"] = True
        elif opt in ("-h", "--help"):
            print(usage)
            sys.exit(0)
        elif opt in ("--api-key"):
            kv["api-key"] = val
        elif opt in ("--start-date"):
            kv["start-date"] = val
        elif opt in ("--end-date"):
            kv["end-date"] = val
        elif opt in ("--stocks"):
            kv["stocks"] = val.split(",")
        elif opt in ("--avg-monthly-open-close"):
            kv["task"] = StockInvestorTask.AVERAGE_MONTHLY_OPEN_CLOSE
        elif opt in ("--max-daily-profit"):
            kv["task"] = StockInvestorTask.MAX_DAILY_PROFIT
        elif opt in ("--busy-day"):
            kv["task"] = StockInvestorTask.BUSY_DAY
        elif opt in ("--biggest-loser"):
            kv["task"] = StockInvestorTask.BIGGEST_LOSER
        else:
            kv["task"] = StockInvestorTask.AVERAGE_MONTHLY_OPEN_CLOSE

    if "api-key" not in kv:
        print("%s: Provide --api-key" % sys.argv[0])
        print(usage)
        sys.exit(2)

    if "stocks" not in kv:
        kv["stocks"] = stock_symbols_default

    start_datetime = yesterday_datetime_default
    try:
        start_datetime = dt.datetime.strptime(kv["start-date"], "%Y-%m-%d")
    except ValueError as ex:
        print(ex)
        print("{}: Invalid --start-date={}".format(sys.argv[0], kv["start-date"]))
        print(usage)
        sys.exit(1)
    except Exception:
        print(sys.stderr)
        sys.exit(1)

    end_datetime = yesterday_datetime_default
    try:
        end_datetime = dt.datetime.strptime(kv["end-date"], "%Y-%m-%d")
    except ValueError as ex:
        print(ex)
        print("{}: Invalid --end-date={}".format(sys.argv[0], kv["end-date"]))
        print(usage)
        sys.exit(1)
    except Exception:
        print(sys.stderr)
        sys.exit(1)

    if start_datetime > end_datetime:
        start_datetime = end_datetime

    if start_datetime > yesterday_datetime_default:
        start_datetime = yesterday_datetime_default
    if end_datetime > yesterday_datetime_default:
        end_datetime = yesterday_datetime_default

    kv["start-datetime"] = start_datetime
    kv["end-datetime"] = end_datetime

    assert kv["api-key"]
    assert kv["start-datetime"]
    assert kv["end-datetime"]

    worker_class = StockInvestor(kv)
    result = worker_class.work()
    pprint(result)

if __name__ == "__main__":
    main()
