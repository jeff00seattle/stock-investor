# stock-investor
Coding challenge
Version: Monday, May 14, 2018 (PDT) 16:30

---

- [Capital One Investing Coding Test Instructions](#capital-one-investing-coding-test-instructions)
- [Investigation of WIKI API](#investigation-of-wiki-api)
- [Development](#development)
  * [Python](#python)
  * [Asynchrous Execution](#asynchrous-execution)
  * [Data Pulled from WIKI API and Cached to memcached](#data-pulled-from-wiki-api-and-cached-to-memcached)
  * [Data Analytics using Python Pandas](#data-analytics-using-python-pandas)
  * [Logging: pyfortified-logging](#logging--pyfortified-logging)
  * [Requests: pyfortified-requests](#requests--pyfortified-requests)
  * [Caching: pyfortified-cache](#caching--pyfortified-cache)
    + [Starting from command line](#starting-from-command-line)
    + [Clearing memcached during testing](#clearing-memcached-during-testing)
  * [Development Issues](#development-issues)
    + [What is Required Next](#what-is-required-next)
- [Application](#application)
  * [Configuration](#configuration)
  * [```--help```](#-----help---)
  * [```--avg-monthly-open-close```](#-----avg-monthly-open-close---)
    + [Python3 Run](#python3-run)
  * [```--max-daily-profit```](#-----max-daily-profit---)
    + [Python3 Run](#python3-run-1)
  * [```--biggest-loser```](#-----biggest-loser---)
    + [Python3 Run](#python3-run-2)
  * [```--busy-day```](#-----busy-day---)
    + [Python3 Run](#python3-run-3)

---

## Capital One Investing Coding Test Instructions

What We Are Looking For:

+ We are looking for production quality code with a high level of software craftsmanship.  We value readable
code that is tested and easy to modify and maintain, over code that runs in the fewest CPU cycles possible.
+ We would like you to write an application that:
  + Retrieves pricing data from the [Quandl WIKI Stock Price API](https://urldefense.proofpoint.com/v2/url?u=https-3A__www.quandl.com_databases_WIKIP&d=DwMFaQ&c=pLULRYW__RtkwsQUPxJVDGboCTdgji3AcHNJU0BpTJE&r=kepIekeKnmUGqfnZNVlrPHu_tMertO2EhArFHfiDIJyCJDfLPZ1NCOioFQV4aw8V&m=mzIO7jy1kzeSyRQcKo83WjUorQBbNrSya7V23VCMgHI&s=p14M8WXuZx6nUbTes6sa2vNtRLwTwfdfwXJTWrptxno&e=) for a given set of securities and date range
  + Displays the **Average Monthly Open and Close** prices for each security for each month of data in the data set.
  + The securities to use are: **COF**, **GOOGL**, and **MSFT**.  Perform this analysis for **Jan - June of 2017**
  + Output the data in the below format, or optionally in a prettier format if you see fit.

```json
{"GOOGL": {"month":"2017-01", "average_open": "815.43", "average_close": "$818.34"},
    {"month":"2017-02", "average_open": "825.87", "average_close": "$822.73"},
    ...
    {"month":"2017-05", "average_open": "945.24", "average_close": "$951.52"},
    {"month":"2017-06", "average_open": "975.37", "average_close": "$977.11"}}
```


The documentation of the API can be found [here](https://www.quandl.com/databases/WIKIP/documentation/about).

You have considerable latitude on how to display this data, obtain it, and what language to use.  Please do this
in the way that feels most comfortable for you. Many candidates prefer to use a script which is run from the
command line. Others choose a webpage that displays things. For others, it’s a live code notebook. What’s
important is that it is well crafted and reproducible by us.

We’d also like you to try and add at least one "additional feature" to this program (and if you’re able, all of them).
They’re listed below as command line switches for a terminal program, but we’d accept any method that lets a
user decide how to display this data.

+ **`--max-daily-profit`**: We’d like to know which day in our data set would provide
the highest amount of profit for each security if purchased at the day’s low and sold at the day’s high.
Please display the ticker symbol, date, and the amount of profit.
+ **`--busy-day`**: We’d like to know which days generated unusually high activity for our securities.
Please display the ticker symbol, date, and volume for each day where the volume was more than 10% higher
than the security’s average volume (Note: You’ll need to calculate the average volume, and should display
that somewhere too).
+ **`--biggest-loser`**: Which security had the most days where the closing price was lower than the
opening price. Please display the ticker symbol and the number of days that security’s closing
price was lower than that day’s opening price.

When you have completed the exercise, please upload your entire solution to Github.com and send
an email with the URL of your repository to COFI_Coding_Exercise@capitalone.com and include your name in the email.
Please make sure you have an appropriate README documenting how we should compile (if necessary) and run your solution.

---

## Investigation of WIKI API

Read the documentation of the API can be found [here](https://www.quandl.com/databases/WIKIP/documentation/about).

And created a bash script for investigating this API.

```bash
$ cd scripts
$cd ./stock_investing.sh \
  --stock GOOGL \
  --api-key [REDACTED] \
  --start-date 2017-01-01 \
  --end-date 2017-06-30 \
  --limit 5 \
  --column-index 5
```

```json
{
  "dataset_data": {
    "limit": 5,
    "transform": null,
    "column_index": 5,
    "column_names": [
      "Date",
      "Volume"
    ],
    "start_date": "2004-08-19",
    "end_date": "2018-03-27",
    "frequency": "daily",
    "data": [
      [
        "2018-03-27",
        2940957
      ],
      [
        "2018-03-26",
        3272409
      ],
      [
        "2018-03-23",
        2413517
      ],
      [
        "2018-03-22",
        3418154
      ],
      [
        "2018-03-21",
        1990515
      ]
    ],
    "collapse": null,
    "order": null
  }
}
```

---

## Development

### Python
This application was built within my Python environment version **3.5.4**:

```bash
$ python3 --version
Python 3.5.4
```

Two Python projects that I  have on PyPi and currently actively developing, however, I have not made sources public yet, where used with this coding challenge:
+ pyfortified-cache: https://pypi.org/project/pyfortified-cache
+ pyfortified-logging: https://pypi.org/project/pyfortified-logging
+ pyfortified-requests: https://pypi.org/project/pyfortified-requests

### Asynchrous Execution

This challenge is using [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) module provides a high-level interface for asynchronously executing callables, which is native to Python 3.x.

### Data Pulled from WIKI API and Cached to memcached

By using memcached, for this exercise, data will be pulled once from WIKI API.

### Data Analytics using Python Pandas

Using cached data, Python Pandas dataframes will be pull from this data and provide requested results.

+ [Python Pandas library](https://pandas.pydata.org/)

### Logging: pyfortified-logging

Extension of Python native logging is used for ease of verbose tracking:

+ https://pypi.org/project/pyfortified-logging

### Requests: pyfortified-requests

Extension of Python project requests is used for more robust HTTP remote calls:

+ https://pypi.org/project/pyfortified-requests/

### Caching: pyfortified-cache

Caching factor with common abstract interface for handling caching fetch/hit/put and cache key generation:

+ https://pypi.org/project/pyfortified-cache/


Install [```memcached```](https://memcached.org/) before before using this application.


#### Starting from command line
```bash
$ memcached
```

#### Clearing memcached during testing
```bash
$ echo 'flush_all' | nc localhost 11211
OK
```

+ [Python + Memcached: Efficient Caching in Distributed Applications](https://realpython.com/python-memcache-efficient-caching)

---

### Development Issues

#### What is Required Next

+ More comments in the code
+ CI Test
+ Bug:Fix overlapping of Cached Date Ranges.


## Application

### Configuration

+ Install Python 3.5+
+ Install memcached and start it
+ Use Makefile to install Python requirements

```bash
$ make install
```

To run application using Makefile, perform the following and add API Key to environment:

```bash
$ export QUANDL_WIKI_API_KEY=[REDACTED]
```

### ```--help```

```bash
$ python3 stock_investing/worker.py --help
Usage: stock_investing/worker.py
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
    --start-date: 'YYYY-MM-DD' Default: '2018-05-13'
    --end-date: 'YYYY-MM-DD' Default: '2018-05-13'
    --stocks: List of WIKI Stock Symbols [Required] Default: ['COF', 'GOOGL', 'MSFT']
    --avg-monthly-open-close: Average Monthly Open and Close prices for each stock. Default.
    --max-daily-profit: Which day provided the highest amount of profit for each stock.
    --busy-day: Which days generated unusually high activity for each stock.
    --biggest-loser: Which stock had the most days where the closing price was lower than the opening price.
 ```

### ```--avg-monthly-open-close```

#### Python3 Run
```bash
python3 stock_investing/worker.py \
  --api-key '[REDACTED]' \
  --start-date '2017-01-01' \
  --end-date '2017-06-30' \
  --avg-monthly-open-close
```

#### Makefile Run
```bash
$ make run-example-avg-monthly-open-close
```

#### Response
```json
{
    'COF': [
        {'average_close': 88.26, 'average_open': 88.3, 'month': '2017-01'},
        {'average_close': 90.2, 'average_open': 89.85, 'month': '2017-02'},
        {'average_close': 88.93, 'average_open': 89.27, 'month': '2017-03'},
        {'average_close': 83.24, 'average_open': 83.41, 'month': '2017-04'},
        {'average_close': 80.51, 'average_open': 80.65, 'month': '2017-05'},
        {'average_close': 80.33, 'average_open': 80.1, 'month': '2017-06'},
    ],
    'GOOGL': [
        {'average_close': 830.25, 'average_open': 829.85, 'month': '2017-01'},
        {'average_close': 836.75, 'average_open': 836.15, 'month': '2017-02'},
        {'average_close': 853.79, 'average_open': 853.86, 'month': '2017-03'},
        {'average_close': 861.38, 'average_open': 860.08, 'month': '2017-04'},
        {'average_close': 961.65, 'average_open': 959.6, 'month': '2017-05'},
        {'average_close': 973.37, 'average_open': 975.78, 'month': '2017-06'},
    ],
    'MSFT': [
        {'average_close': 63.19, 'average_open': 63.19, 'month': '2017-01'},
        {'average_close': 64.11, 'average_open': 64.13, 'month': '2017-02'},
        {'average_close': 64.84, 'average_open': 64.76, 'month': '2017-03'},
        {'average_close': 66.17, 'average_open': 66.24, 'month': '2017-04'},
        {'average_close': 68.92, 'average_open': 68.83, 'month': '2017-05'},
        {'average_close': 70.52, 'average_open': 70.56, 'month': '2017-06'},
    ],
}
```

### ```--max-daily-profit```

#### Python3 Run
```bash
python3 stock_investing/worker.py \
  --api-key '[REDACTED]' \
  --start-date '2017-01-01' \
  --end-date '2017-06-30' \
  --max-daily-profit
```

#### Makefile Run
```bash
$ make run-example-max-daily-profit
```

#### Response
```json
{
    'COF': {'Date': '2017-03-21', 'Profit': 3.76},
    'GOOGL': {'Date': '2017-06-09', 'Profit': 52.13},
    'MSFT': {'Date': '2017-06-09', 'Profit': 3.49},
}
```

### ```--biggest-loser```

Which security had the most days where the closing price was lower than the
opening price. Please display the ticker symbol and the number of days that security’s closing
price was lower than that day’s opening price.

#### Python3 Run
```bash
$ python3 stock_investing/worker.py \
  --api-key '[REDACTED]' \
  --start-date '2017-01-01' \
  --end-date '2017-06-30' \
  --biggest-loser
```

#### Makefile Run
```bash
$ make run-example-biggest-loser
```

#### Response
```json
{'COF': 62}
```

### ```--busy-day```

We’d like to know which days generated unusually high activity for our securities.
Please display the ticker symbol, date, and volume for each day where the volume was more than 10% higher
than the security’s average volume (Note: You’ll need to calculate the average volume, and should display
that somewhere too).

#### Python3 Run
```bash
python3 stock_investing/worker.py \
  --api-key '[REDACTED]' \
  --start-date '2017-01-01' \
  --end-date '2017-06-30' \
  --busy-day
```

#### Makefile Run
```bash
$ make run-example-busy-day
```

#### Response
```json
{
    'COF': [
        {'date': '2017-05-12', 'volume': 3931119, 'volume_mean': 2757167},
        {'date': '2017-06-19', 'volume': 3225890, 'volume_mean': 2757167},
        {'date': '2017-03-22', 'volume': 3133651, 'volume_mean': 2757167},
        {'date': '2017-03-17', 'volume': 3388267, 'volume_mean': 2757167},
        {'date': '2017-04-25', 'volume': 3080861, 'volume_mean': 2757167},
        {'date': '2017-01-25', 'volume': 5304078, 'volume_mean': 2757167},
        {'date': '2017-02-07', 'volume': 3514042, 'volume_mean': 2757167},
        {'date': '2017-04-13', 'volume': 3400095, 'volume_mean': 2757167},
        {'date': '2017-03-15', 'volume': 3178963, 'volume_mean': 2757167},
        {'date': '2017-06-01', 'volume': 3295232, 'volume_mean': 2757167},
        {'date': '2017-01-03', 'volume': 3441067, 'volume_mean': 2757167},
        {'date': '2017-05-18', 'volume': 4884650, 'volume_mean': 2757167},
        {'date': '2017-06-15', 'volume': 3854218, 'volume_mean': 2757167},
        {'date': '2017-04-03', 'volume': 3158771, 'volume_mean': 2757167},
        {'date': '2017-04-26', 'volume': 7386158, 'volume_mean': 2757167},
        {'date': '2017-05-04', 'volume': 3154418, 'volume_mean': 2757167},
        {'date': '2017-04-06', 'volume': 4378949, 'volume_mean': 2757167},
        {'date': '2017-05-31', 'volume': 4205013, 'volume_mean': 2757167},
        {'date': '2017-03-30', 'volume': 4081656, 'volume_mean': 2757167},
        {'date': '2017-04-17', 'volume': 3759420, 'volume_mean': 2757167},
        {'date': '2017-03-01', 'volume': 3387946, 'volume_mean': 2757167},
        {'date': '2017-01-10', 'volume': 3141198, 'volume_mean': 2757167},
        {'date': '2017-03-27', 'volume': 4282097, 'volume_mean': 2757167},
        {'date': '2017-05-01', 'volume': 3543401, 'volume_mean': 2757167},
        {'date': '2017-06-29', 'volume': 6009615, 'volume_mean': 2757167},
        {'date': '2017-05-17', 'volume': 3145845, 'volume_mean': 2757167},
        {'date': '2017-04-28', 'volume': 6133211, 'volume_mean': 2757167},
        {'date': '2017-03-21', 'volume': 4559025, 'volume_mean': 2757167},
        {'date': '2017-06-16', 'volume': 3255538, 'volume_mean': 2757167},
        {'date': '2017-02-28', 'volume': 3122357, 'volume_mean': 2757167},
        {'date': '2017-04-18', 'volume': 3119402, 'volume_mean': 2757167},
        {'date': '2017-05-11', 'volume': 3741154, 'volume_mean': 2757167},
        {'date': '2017-04-27', 'volume': 3604560, 'volume_mean': 2757167},
        {'date': '2017-01-30', 'volume': 3550371, 'volume_mean': 2757167},
        {'date': '2017-06-09', 'volume': 3476989, 'volume_mean': 2757167},
        {'date': '2017-06-28', 'volume': 3773097, 'volume_mean': 2757167},
        {'date': '2017-03-28', 'volume': 3784720, 'volume_mean': 2757167},
        {'date': '2017-02-21', 'volume': 3825225, 'volume_mean': 2757167},
        {'date': '2017-02-17', 'volume': 4044661, 'volume_mean': 2757167},
    ],
    'GOOGL': [
        {'date': '2017-01-27', 'volume': 3752497, 'volume_mean': 1632363},
        {'date': '2017-05-01', 'volume': 2294856, 'volume_mean': 1632363},
        {'date': '2017-03-17', 'volume': 1868252, 'volume_mean': 1632363},
        {'date': '2017-06-12', 'volume': 4167184, 'volume_mean': 1632363},
        {'date': '2017-02-01', 'volume': 2251047, 'volume_mean': 1632363},
        {'date': '2017-03-23', 'volume': 3287669, 'volume_mean': 1632363},
        {'date': '2017-03-27', 'volume': 1935211, 'volume_mean': 1632363},
        {'date': '2017-06-16', 'volume': 2484914, 'volume_mean': 1632363},
        {'date': '2017-06-29', 'volume': 3182331, 'volume_mean': 1632363},
        {'date': '2017-06-28', 'volume': 2713366, 'volume_mean': 1632363},
        {'date': '2017-01-03', 'volume': 1959033, 'volume_mean': 1632363},
        {'date': '2017-06-15', 'volume': 2349212, 'volume_mean': 1632363},
        {'date': '2017-04-03', 'volume': 1969402, 'volume_mean': 1632363},
        {'date': '2017-04-05', 'volume': 1855153, 'volume_mean': 1632363},
        {'date': '2017-05-04', 'volume': 1934652, 'volume_mean': 1632363},
        {'date': '2017-04-25', 'volume': 2020460, 'volume_mean': 1632363},
        {'date': '2017-05-17', 'volume': 2414323, 'volume_mean': 1632363},
        {'date': '2017-01-06', 'volume': 2017097, 'volume_mean': 1632363},
        {'date': '2017-05-08', 'volume': 1863198, 'volume_mean': 1632363},
        {'date': '2017-03-01', 'volume': 1818671, 'volume_mean': 1632363},
        {'date': '2017-06-13', 'volume': 1992456, 'volume_mean': 1632363},
        {'date': '2017-01-23', 'volume': 2457377, 'volume_mean': 1632363},
        {'date': '2017-01-26', 'volume': 3493251, 'volume_mean': 1632363},
        {'date': '2017-04-28', 'volume': 3753169, 'volume_mean': 1632363},
        {'date': '2017-03-21', 'volume': 2537978, 'volume_mean': 1632363},
        {'date': '2017-01-31', 'volume': 2020180, 'volume_mean': 1632363},
        {'date': '2017-05-25', 'volume': 1951402, 'volume_mean': 1632363},
        {'date': '2017-04-27', 'volume': 1817740, 'volume_mean': 1632363},
        {'date': '2017-01-30', 'volume': 3516933, 'volume_mean': 1632363},
        {'date': '2017-06-09', 'volume': 3613964, 'volume_mean': 1632363},
        {'date': '2017-06-30', 'volume': 2185444, 'volume_mean': 1632363},
        {'date': '2017-06-27', 'volume': 2428048, 'volume_mean': 1632363},
        {'date': '2017-03-24', 'volume': 2105682, 'volume_mean': 1632363},
    ],
    'MSFT': [
        {'date': '2017-01-20', 'volume': 30213462, 'volume_mean': 23748646},
        {'date': '2017-01-27', 'volume': 44817972, 'volume_mean': 23748646},
        {'date': '2017-05-01', 'volume': 31304672, 'volume_mean': 23748646},
        {'date': '2017-03-17', 'volume': 49219686, 'volume_mean': 23748646},
        {'date': '2017-05-15', 'volume': 30705323, 'volume_mean': 23748646},
        {'date': '2017-02-01', 'volume': 39671528, 'volume_mean': 23748646},
        {'date': '2017-06-16', 'volume': 46911637, 'volume_mean': 23748646},
        {'date': '2017-05-16', 'volume': 33250702, 'volume_mean': 23748646},
        {'date': '2017-06-12', 'volume': 47363986, 'volume_mean': 23748646},
        {'date': '2017-05-11', 'volume': 27985424, 'volume_mean': 23748646},
        {'date': '2017-06-06', 'volume': 31220057, 'volume_mean': 23748646},
        {'date': '2017-04-25', 'volume': 29983174, 'volume_mean': 23748646},
        {'date': '2017-05-31', 'volume': 29538356, 'volume_mean': 23748646},
        {'date': '2017-04-19', 'volume': 26992771, 'volume_mean': 23748646},
        {'date': '2017-05-17', 'volume': 29964198, 'volume_mean': 23748646},
        {'date': '2017-06-05', 'volume': 29507429, 'volume_mean': 23748646},
        {'date': '2017-03-01', 'volume': 26937459, 'volume_mean': 23748646},
        {'date': '2017-02-03', 'volume': 30301759, 'volume_mean': 23748646},
        {'date': '2017-04-24', 'volume': 29721254, 'volume_mean': 23748646},
        {'date': '2017-06-02', 'volume': 34586054, 'volume_mean': 23748646},
        {'date': '2017-01-26', 'volume': 43554645, 'volume_mean': 23748646},
        {'date': '2017-04-28', 'volume': 38940853, 'volume_mean': 23748646},
        {'date': '2017-03-21', 'volume': 26640480, 'volume_mean': 23748646},
        {'date': '2017-02-02', 'volume': 45827013, 'volume_mean': 23748646},
        {'date': '2017-06-29', 'volume': 28231562, 'volume_mean': 23748646},
        {'date': '2017-04-21', 'volume': 32522645, 'volume_mean': 23748646},
        {'date': '2017-01-30', 'volume': 31651445, 'volume_mean': 23748646},
        {'date': '2017-06-09', 'volume': 48619420, 'volume_mean': 23748646},
        {'date': '2017-05-19', 'volume': 26496478, 'volume_mean': 23748646},
        {'date': '2017-04-27', 'volume': 32219234, 'volume_mean': 23748646},
        {'date': '2017-05-03', 'volume': 28725646, 'volume_mean': 23748646},
    ],
}
```
