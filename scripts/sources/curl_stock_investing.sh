#!/usr/bin/env bash

if [ -z "$CURL_REQUEST" ]
  then
    CURL_REQUEST="GET"
fi

CURL_VERBOSE=""
if [ $VERBOSE = true ]
  then
    CURL_VERBOSE=" --verbose"
fi

CURL_CMD="curl \"https://www.quandl.com/api/v3/datasets/WIKI/${STOCK}/data.json?${QUERY_STRING}\"
  --request $CURL_REQUEST
  $CURL_VERBOSE
  --header \"Content-Type: application/json\"
  --connect-timeout 60
  --location
  --get
  --write-out \"%{time_total}\n\"
"

if [ $VERBOSE = true ]
  then
    echo CURL_CMD=$CURL_CMD
fi

CURL_RESPONSE=$(eval $CURL_CMD)