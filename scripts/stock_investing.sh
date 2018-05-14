#!/usr/bin/env bash
#  Algorithmia Interview
#

VERBOSE=false
STOCK=""
API_KEY=""
START_DATE=""
END_DATE=""
COLUMN_INDEX=0
LIMIT=0
QUERY_STRING=""

USAGE="\nUsage: $0\n
[-v|--verbose]\n
[-h|--help]\n
[--stock <string>]\n
[--api-key <string>]\n
[--start-date <string>]\n
[--end-date <string>]\n
[--limit <int>]\n
[--column-index <int>]\n"

usage() { echo -e $USAGE 1>&2; exit 1; }

# read the options
OPTS=`getopt -o vh --long verbose,help,stock:,api-key:,start-date:,end-date:,limit:,column-index: -n 'stock_investing.sh' -- "$@"`
if [ $? != 0 ] ; then echo "Failed parsing options." >&2 ; usage ; exit 1 ; fi
eval set -- "$OPTS"


# extract options and their arguments into variables.
for i
do
  case "$i"
  in
    -v|--verbose)
      VERBOSE=true ;
      shift ;;
    -h|--help)
      usage ;;
    --stock)
      STOCK="$2" ;
      shift 2 ;;
    --api-key)
      API_KEY="$2" ;
      QUERY_STRING+="api_key=$API_KEY&"
      shift 2 ;;
    --start-date)
      START_DATE="$2" ;
      QUERY_STRING+="start_date=$START_DATE&"
      shift 2 ;;
    --end-date)
      END_DATE="$2" ;
      QUERY_STRING+="end_date=$END_DATE&"
      shift 2 ;;
    --limit)
      LIMIT="$2" ;
      QUERY_STRING+="limit=$LIMIT&"
      shift 2 ;;
    --column-index)
      COLUMN_INDEX="$2" ;
      QUERY_STRING+="column_index=$COLUMN_INDEX&"
      shift 2 ;;
  esac
done

if [ -z "$STOCK" ]
  then
    echo "$0: Provide --stock" ; usage ; exit 1
fi

if [ -z "$API_KEY" ]
  then
    echo "$0: Provide --api-key" ; usage ; exit 1
fi

if [ -z "$START_DATE" ]
  then
    echo "$0: Provide --start-date" ; usage ; exit 1
fi

if [ -z "$END_DATE" ]
  then
    echo "$0: Provide --end-date" ; usage ; exit 1
fi

if [ $VERBOSE = true ]
  then
    echo VERBOSE=$VERBOSE
    echo HELP=$HELP
    echo STOCK=$STOCK
    echo QUERY_STRING=$QUERY_STRING
fi

source sources/curl_stock_investing.sh

echo $CURL_RESPONSE | jq
