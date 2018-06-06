# coding:utf8
# from __future__ import unicode_literals, print_function, division

import json


from . import helpers

from .log import log

import requests


class XueQiu(object):
    LOGIN_PAGE      = 'https://www.xueqiu.com'
    LOGIN_API       = 'https://xueqiu.com/snowman/login'
    TRANSACTION_API = 'https://xueqiu.com/cubes/rebalancing/history.json'
    PORTFOLIO_URL   = 'https://xueqiu.com/p/'
    WEB_REFERER     = 'https://www.xueqiu.com'
    WEB_ORIGIN      = ''
    STOCK_INFO      = 'https://xueqiu.com/v4/stock/quote.json?code={}'

    def __init__(self):
        self.s = requests.Session()

    def session(self):
        return self.s

    def login(self, **kwargs):
        """
        雪球登陆， 需要设置 cookies
        :param cookies: 雪球登陆需要设置 cookies， 具体见
            https://smalltool.github.io/2016/08/02/cookie/
        :return:
        """
        cookies = kwargs.get('cookies')
        if cookies is None:
            raise TypeError('雪球登陆需要设置 cookies， 具体见'
                            'https://smalltool.github.io/2016/08/02/cookie/')
        headers = self._generate_headers()
        self.s.headers.update(headers)

        cookie_dict = helpers.parse_cookies_str(cookies)
        self.s.cookies.update(cookie_dict)

        # print(self._get_stock_rise_stop_price('sz300477'))
        # print(self._get_stock_fall_stop_price('sz300477'))
        
        # log.info('雪球登录成功')

    def _generate_headers(self):
        headers = {
            'Accept':
            'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':
            'gzip, deflate, br',
            'Accept-Language':
            'en-US,en;q=0.8',
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/54.0.2840.100 Safari/537.36',
            'Referer':
            self.WEB_REFERER,
            'X-Requested-With':
            'XMLHttpRequest',
            'Origin':
            self.WEB_ORIGIN,
            'Content-Type':
            'application/x-www-form-urlencoded; charset=UTF-8',
        }
        return headers


    def _get_stock_rise_stop_price(self, security):
        url = self.STOCK_INFO.format(security)
        res = self.s.get(url)
        data = res.json()
        # print(data)

        security_upper = security.upper()
        # print('ly: ', data[security_upper]['rise_stop'])
        # print('ly2: ', float(data[security_upper]['rise_stop']))
        return float(data[security_upper]['rise_stop'])

    def _get_stock_fall_stop_price(self, security):
        url = self.STOCK_INFO.format(security)
        res = self.s.get(url)
        data = res.json()

        security_upper = security.upper()
        return float(data[security_upper]['fall_stop'])
