# coding:utf8
from __future__ import division

import re
import tempfile
import time

import pywinauto
import pywinauto.clipboard

from . import helpers
from .clienttrader import ClientTrader
import easyutils

from . import Xueqiu


class GJClientTrader(ClientTrader):
    @property
    def broker_type(self):
        return 'gj'

    def setXueqiu(self, xq):
        self.xq = xq

    def login(self, user, password, exe_path, comm_password=None, **kwargs):
        """
        登陆客户端
        :param user: 账号
        :param password: 明文密码
        :param exe_path: 客户端路径类似 r'C:\中国银河证券双子星3.2\Binarystar.exe', 默认 r'C:\中国银河证券双子星3.2\Binarystar.exe'
        :param comm_password: 通讯密码, 华泰需要，可不设
        :return:
        """
        try:
            self._app = pywinauto.Application().connect(
                path=self._run_exe_path(exe_path), timeout=1)
        except Exception:
            self._app = pywinauto.Application().start(exe_path)

            # wait login window ready
            while True:
                try:
                    self._app.top_window().Edit1.wait('ready')
                    break
                except RuntimeError:
                    pass

            self._app.top_window().Edit1.type_keys(user)
            self._app.top_window().Edit2.type_keys(password)
            edit3 = self._app.top_window().window(control_id=0x3eb)
            while True:
                try:
                    code = self._handle_verify_code()
                    edit3.type_keys(code)
                    time.sleep(1)
                    self._app.top_window()['确定(Y)'].click()
                    # detect login is success or not
                    try:
                        self._app.top_window().wait_not('exists', 5)
                        break
                    except:
                        self._app.top_window()['确定'].click()
                        pass
                except Exception as e:
                    pass

            self._app = pywinauto.Application().connect(
                path=self._run_exe_path(exe_path), timeout=10)
        self._main = self._app.window(title='网上股票交易系统5.0')

    def _handle_verify_code(self):
        control = self._app.top_window().window(control_id=0x5db)
        control.click()
        time.sleep(0.2)
        file_path = tempfile.mktemp() + '.jpg'
        control.capture_as_image().save(file_path)
        time.sleep(0.2)
        vcode = helpers.recognize_verify_code(file_path, 'gj_client')
        return ''.join(re.findall('[a-zA-Z0-9]+', vcode))

    def buy(self, security, price, amount, **kwargs):
        print('Lewis Buy function')
        weight = kwargs['weight']
        if weight == 0:
            print ('weight is 0, we will not buy anything')
        else:
            price = self._adjust_buy_price(security, price)#less than 3 point
            total_asset = self.balance()[0]['资金余额']#need test
            amount = int(total_asset/price)/100*100#need test

            self._switch_left_menus(['买入[F1]'])

            return self.trade(security, price, amount)

    def _adjust_buy_price(self, security, price):
        price_preset    = price * (1+0.15)
        price_up_stop = self._get_stock_up_stop_price(security)

        price_min = min(price_preset, price_up_stop)

        return easyutils.round_price_by_code(price_min, security)

    def _get_stock_up_stop_price(self, security):
        return self.xq._get_stock_rise_stop_price(security)
        


    def sell(self, security, price, amount, **kwargs):
        print('Lewis Sell function')
        weight = kwargs['weight']
        if weight == 0:
            print ('weight is 0, we will not sell anything')
        else:
            price  = self._adjust_sell_price(security, price)
            amount = self.position[0]['当前持仓']

            self._switch_left_menus(['卖出[F2]'])

            return self.trade(security, price, amount)


    def _adjust_sell_price(self, security, price):
        price_preset    = price * (1-0.15)
        price_down_stop = self._get_stock_down_stop_price(security)

        price_max = max(price_preset, price_down_stop)

        return easyutils.round_price_by_code(price_max, security)

    def _get_stock_down_stop_price(self, security):
        return self.xq._get_stock_fall_stop_price(security)