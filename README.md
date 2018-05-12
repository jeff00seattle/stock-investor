# stock-investor
Coding challenge
Version: Saturday, May 12, 2018 (PDT) 14:00
    
---

  * [Capital One Investing Coding Test Instructions](#capital-one-investing-coding-test-instructions)
  * [Investigation of WIKI API](#investigation-of-wiki-api)
  * [Development](#development)
    + [Python](#python)
    + [Data Pulled from WIKI API and Cached to memcached](#data-pulled-from-wiki-api-and-cached-to-memcached)
    + [Data Analytics using Python Pandas](#data-analytics-using-python-pandas)
    + [```memcached```](#---memcached---)
    + [Development Issues](#development-issues)
      - [Panda Warning: ```SettingWithCopyWarning```](#panda-warning-----settingwithcopywarning---)
      - [What is Required Next](#what-is-required-next)
  * [Application](#application)
    + [Configuration](#configuration)
    + [```--help```](#-----help---)
    + [```--avg-monthly```](#-----avg-monthly---)
      - [Python3 Run](#python3-run)
      - [Known Issues: Python Pandas Warning: ```SettingWithCopyWarning```](#known-issues--python-pandas-warning-----settingwithcopywarning---)
    + [```--max-daily-profit```](#-----max-daily-profit---)
      - [Python3 Run](#python3-run-1)
    + [```--biggest-loser```](#-----biggest-loser---)
      - [Python3 Run](#python3-run-2)
    + [```--busy-day```](#-----busy-day---)
      - [Python3 Run](#python3-run-3)
    
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
This application will be built on two Python packages I currently have in Open Source Development, however, I have not made sources public yet:
+ https://pypi.org/project/logging-fortified/
+ https://pypi.org/project/requests-fortified/

### Data Pulled from WIKI API and Cached to memcached

By using memcached, for this exercise, data will be pulled once from WIKI API.

### Data Analytics using Python Pandas

Using cached data, Python Pandas dataframes will be pull from this data and provide requested results.

+ [Python Pandas library](https://pandas.pydata.org/)

### ```memcached```

Install and start before using this application.

https://realpython.com/python-memcache-efficient-caching/

```bash
$ memcached
```

```bash
$ echo 'flush_all' | nc localhost 11211
OK
```

+ [Python + Memcached: Efficient Caching in Distributed Applications](https://realpython.com/python-memcache-efficient-caching)
+ [Memcached](https://memcached.org/)

https://memcached.org/

---

### Development Issues

#### Panda Warning: ```SettingWithCopyWarning```

```bash
/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/pandas/core/indexing.py:357: SettingWithCopyWarning:
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead
```

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
       [--help | --avg-monthly | --max-daily-profit | --busy-day | --biggest-loser]
    -v | --verbose: Provide verbose details
    -h | --help: Usage
    --api-key: Quandl WIKI API Key [Required]
    --start-date: 'YYYY-MM-DD' Default: '2018-05-11'
    --end-date: 'YYYY-MM-DD' Default: '2018-05-11'
    --stocks: List of WIKI Stock Symbols [Required] Default: ['COF', 'GOOGL', 'MSFT']
    --avg-monthly: Average Monthly Open and Close prices for each stock. Default.
    --max-daily-profit: Which day provided the highest amount of profit for each stock.
    --busy-day: Which days generated unusually high activity for each stock.
    --biggest-loser: Which stock had the most days where the closing price was lower than the opening price.
 ```

### ```--avg-monthly```

#### Python3 Run
```bash
python3 stock_investing/worker.py \
  --api-key '[REDACTED]' \
  --start-date '2017-01-01' \
  --end-date '2017-06-30' \
  --avg-monthly
```

```json
{
    'COF': [
        {'average_close': 88.26, 'average_open': 88.2985, 'month': '2017-01'},
        {
            'average_close': 90.19578947368421,
            'average_open': 89.85263157894737,
            'month': '2017-02',
        },
        {
            'average_close': 88.92521739130437,
            'average_open': 89.26782608695652,
            'month': '2017-03',
        },
        {
            'average_close': 83.23526315789472,
            'average_open': 83.41105263157895,
            'month': '2017-04',
        },
        {
            'average_close': 80.50863636363636,
            'average_open': 80.64818181818183,
            'month': '2017-05',
        },
        {
            'average_close': 80.32818181818183,
            'average_open': 80.09818181818181,
            'month': '2017-06',
        },
    ],
    'GOOGL': [
        {
            'average_close': 830.2495000000001,
            'average_open': 829.8539999999997,
            'month': '2017-01',
        },
        {
            'average_close': 836.7547368421052,
            'average_open': 836.1510526315789,
            'month': '2017-02',
        },
        {
            'average_close': 853.7897826086955,
            'average_open': 853.8582608695652,
            'month': '2017-03',
        },
        {
            'average_close': 861.3776315789474,
            'average_open': 860.0765789473684,
            'month': '2017-04',
        },
        {
            'average_close': 961.6545454545453,
            'average_open': 959.595909090909,
            'month': '2017-05',
        },
        {
            'average_close': 973.3727272727272,
            'average_open': 975.781818181818,
            'month': '2017-06',
        },
    ],
    'MSFT': [
        {
            'average_close': 63.19200000000001,
            'average_open': 63.185500000000005,
            'month': '2017-01',
        },
        {
            'average_close': 64.1136842105263,
            'average_open': 64.13447368421052,
            'month': '2017-02',
        },
        {
            'average_close': 64.84130434782608,
            'average_open': 64.76434782608695,
            'month': '2017-03',
        },
        {
            'average_close': 66.17157894736842,
            'average_open': 66.23894736842107,
            'month': '2017-04',
        },
        {
            'average_close': 68.91772727272729,
            'average_open': 68.82818181818182,
            'month': '2017-05',
        },
        {
            'average_close': 70.51795454545454,
            'average_open': 70.56136363636362,
            'month': '2017-06',
        },
    ],
}
```

#### Known Issues: Python Pandas Warning: ```SettingWithCopyWarning```

```bash
/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/pandas/core/indexing.py:357: SettingWithCopyWarning:
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead
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

```json
[
    {'Date': '2017-03-21', 'Profit': 3.76, 'Stock': 'COF'},
    {'Date': '2017-06-09', 'Profit': 52.13, 'Stock': 'GOOGL'},
    {'Date': '2017-06-09', 'Profit': 3.49, 'Stock': 'MSFT'},
]
```

### ```--biggest-loser```


#### Python3 Run

```bash
$ python3 stock_investing/worker.py \
  --api-key '[REDACTED]' \
  --start-date '2017-01-01' \
  --end-date '2017-06-30' \
  --biggest-loser
```

```json
{'COF': 62}
```

### ```--busy-day```

#### Python3 Run

```bash
python3 stock_investing/worker.py \
  --api-key '[REDACTED]' \
  --start-date '2017-01-01' \
  --end-date '2017-06-30' \
  --busy-day
```

```json
[
    {
        'COF': [
            {
                'date': '2017-01-03',
                'volume_high': 24.8044018338,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-01-10',
                'volume_high': 13.928423198800001,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-01-25',
                'volume_high': 92.3741333923,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-01-30',
                'volume_high': 28.768759499,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-02-07',
                'volume_high': 27.4511393788,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-02-17',
                'volume_high': 46.6962127519,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-02-21',
                'volume_high': 38.7374666069,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-02-28',
                'volume_high': 13.2450770928,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-03-01',
                'volume_high': 22.8777509927,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-03-15',
                'volume_high': 15.2981257461,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-03-17',
                'volume_high': 22.8893933737,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-03-21',
                'volume_high': 65.3517319106,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-03-22',
                'volume_high': 13.654700304,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-03-27',
                'volume_high': 55.3078026901,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-03-28',
                'volume_high': 37.2683867267,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-03-30',
                'volume_high': 48.0379880925,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-04-03',
                'volume_high': 14.5657800865,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-04-06',
                'volume_high': 58.8205375268,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-04-13',
                'volume_high': 23.318384284,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-04-17',
                'volume_high': 36.3507785062,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-04-18',
                'volume_high': 13.1379019034,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-04-25',
                'volume_high': 11.7400545349,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-04-26',
                'volume_high': 167.8893003362,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-04-27',
                'volume_high': 30.7341457385,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-04-28',
                'volume_high': 122.4460407704,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-05-01',
                'volume_high': 28.5159638747,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-05-04',
                'volume_high': 14.4079006959,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-05-11',
                'volume_high': 35.6882871325,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-05-12',
                'volume_high': 42.5781466425,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-05-17',
                'volume_high': 14.0969657048,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-05-18',
                'volume_high': 77.1618574755,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-05-31',
                'volume_high': 52.5120354147,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-06-01',
                'volume_high': 19.5150976902,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-06-09',
                'volume_high': 26.1072604305,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-06-15',
                'volume_high': 39.7890166123,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-06-16',
                'volume_high': 18.0754320498,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-06-19',
                'volume_high': 17.0001257841,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-06-28',
                'volume_high': 36.8468309818,
                'volume_mean': 2757167.976,
            },
            {
                'date': '2017-06-29',
                'volume_high': 117.9633251333,
                'volume_mean': 2757167.976,
            },
        ],
    },
    {
        'GOOGL': [
            {
                'date': '2017-01-03',
                'volume_high': 20.0120417282,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-01-06',
                'volume_high': 23.5690921663,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-01-23',
                'volume_high': 50.5410225688,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-01-26',
                'volume_high': 113.9995522174,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-01-27',
                'volume_high': 129.8811845176,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-01-30',
                'volume_high': 115.4503318481,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-01-31',
                'volume_high': 23.7579593904,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-02-01',
                'volume_high': 37.9010698116,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-03-01',
                'volume_high': 11.4133452279,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-03-17',
                'volume_high': 14.4507198107,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-03-21',
                'volume_high': 55.4787089556,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-03-23',
                'volume_high': 101.4054225818,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-03-24',
                'volume_high': 28.9958852405,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-03-27',
                'volume_high': 18.5526855775,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-04-03',
                'volume_high': 20.6472555611,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-04-05',
                'volume_high': 13.6482638364,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-04-25',
                'volume_high': 23.7751124306,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-04-27',
                'volume_high': 11.3563113695,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-04-28',
                'volume_high': 129.9223518139,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-05-01',
                'volume_high': 40.584846724,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-05-04',
                'volume_high': 18.5184407581,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-05-08',
                'volume_high': 14.1411074361,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-05-17',
                'volume_high': 47.9034976039,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-05-25',
                'volume_high': 19.5445601236,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-06-09',
                'volume_high': 121.3945341259,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-06-12',
                'volume_high': 155.2852657904,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-06-13',
                'volume_high': 22.0595633732,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-06-15',
                'volume_high': 43.914741902,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-06-16',
                'volume_high': 52.2279628057,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-06-27',
                'volume_high': 48.744302875,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-06-28',
                'volume_high': 66.2231282556,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-06-29',
                'volume_high': 94.9523263595,
                'volume_mean': 1632363.696,
            },
            {
                'date': '2017-06-30',
                'volume_high': 33.8821737677,
                'volume_mean': 1632363.696,
            },
        ],
    },
    {
        'MSFT': [
            {
                'date': '2017-01-20',
                'volume_high': 27.22182464,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-01-26',
                'volume_high': 83.3984271133,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-01-27',
                'volume_high': 88.7180017472,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-01-30',
                'volume_high': 33.2768348557,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-02-01',
                'volume_high': 67.0475292906,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-02-02',
                'volume_high': 92.9668374866,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-02-03',
                'volume_high': 27.5936226633,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-03-01',
                'volume_high': 13.4273419294,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-03-17',
                'volume_high': 107.25259029,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-03-21',
                'volume_high': 12.1768327934,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-04-19',
                'volume_high': 13.6602478296,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-04-21',
                'volume_high': 36.945254371,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-04-24',
                'volume_high': 25.1492518292,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-04-25',
                'volume_high': 26.2521357128,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-04-27',
                'volume_high': 35.6676615868,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-04-28',
                'volume_high': 63.9708276959,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-05-01',
                'volume_high': 31.8166548275,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-05-03',
                'volume_high': 20.9569793122,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-05-11',
                'volume_high': 17.8400775325,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-05-15',
                'volume_high': 29.292936315,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-05-16',
                'volume_high': 40.0109321799,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-05-17',
                'volume_high': 26.1722322134,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-05-19',
                'volume_high': 11.5704740388,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-05-31',
                'volume_high': 24.3791111123,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-06-02',
                'volume_high': 45.6337872494,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-06-05',
                'volume_high': 24.248884746,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-06-06',
                'volume_high': 31.4603608453,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-06-09',
                'volume_high': 104.7250105049,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-06-12',
                'volume_high': 99.4386714486,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-06-16',
                'volume_high': 97.5339355678,
                'volume_mean': 23748646.968,
            },
            {
                'date': '2017-06-29',
                'volume_high': 18.8765071039,
                'volume_mean': 23748646.968,
            },
        ],
    },
]
```
