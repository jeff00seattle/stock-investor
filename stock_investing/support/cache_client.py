#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @namespace stock_investing

import ujson as json
from .errors_traceback import get_exception_message
from pymemcache.client import base

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
