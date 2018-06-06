

from six.moves.queue import Queue
from .log import log
from threading import Thread
from datetime import datetime
import time

from . import exceptions

class TraderBridge(object):

	def __init__(self, queue, users = []):
		self.queue = queue
		self.users = self.warp_list(users)

	@staticmethod
	def warp_list(value):
		if not isinstance(value, list):
			value=[value]
		return value

	def trade(self,
              trade_cmd_expire_seconds = 120,
              entrust_prop='limit',
              send_interval=0):
		trader=Thread(
			target=self.trade_worker,
            kwargs={
                'expire_seconds': trade_cmd_expire_seconds,
                'entrust_prop': entrust_prop,
                'send_interval': send_interval
            })
		trader.setDaemon(True)
		trader.start()
		print('traderBridge')

	def trade_worker(self,
		expire_seconds=120,
		entrust_prop='limit',
		send_interval=0):
		"""
		:param send_interval: 交易发送间隔,默认为0s。调大可防止卖出买入时买出单没有及时成交导致的买入金额不足
		"""
		while True:
			trade_cmd = self.queue.get()
			self._execute_trade_cmd(trade_cmd, expire_seconds,
				entrust_prop, send_interval)
			time.sleep(send_interval)

	def _execute_trade_cmd(self, trade_cmd, expire_seconds,
		entrust_prop, send_interval):
		"""分发交易指令到对应的 user 并执行
		:param trade_cmd:
		:param users:
		:param expire_seconds:
		:param entrust_prop:
		:param send_interval:
		:return:
		"""
		for user in self.users:
			# check expire
			now = datetime.now()
			expire = (now - trade_cmd['datetime']).total_seconds()
			# if expire > expire_seconds:
			# 	log.warning(
			# 		'策略 [{}] 指令(股票: {} 动作: {} 数量: {} 价格: {})超时，指令产生时间: {} 当前时间: {}, 超过设置的最大过期时间 {} 秒, 被丢弃'.
			# 		format(trade_cmd['strategy_name'], trade_cmd['stock_code'],
			# 			trade_cmd['action'], trade_cmd['amount'],
			# 			trade_cmd['price'], trade_cmd['datetime'], now,
			# 			expire_seconds))
			# 	break

			# # check price
			# price = trade_cmd['price']
			# if not self._is_number(price) or price <= 0:
			# 	log.warning(
			# 		'策略 [{}] 指令(股票: {} 动作: {} 数量: {} 价格: {})超时，指令产生时间: {} 当前时间: {}, 价格无效 , 被丢弃'.
			# 		format(trade_cmd['strategy_name'], trade_cmd['stock_code'],
			# 			trade_cmd['action'], trade_cmd['amount'],
			# 			trade_cmd['price'], trade_cmd['datetime'], now))
			# 	break

			# # check amount
			# if trade_cmd['amount'] <= 0:
			# 	log.warning(
			# 		'策略 [{}] 指令(股票: {} 动作: {} 数量: {} 价格: {})超时，指令产生时间: {} 当前时间: {}, 买入股数无效 , 被丢弃'.
			# 		format(trade_cmd['strategy_name'], trade_cmd['stock_code'],
			# 			trade_cmd['action'], trade_cmd['amount'],
			# 			trade_cmd['price'], trade_cmd['datetime'], now))
			# 	break

			args = {
			'security': trade_cmd['stock_code'],
			'price': trade_cmd['price'],
			'amount': trade_cmd['amount'],
			'weight': trade_cmd['delta_weight'],
			'entrust_prop': entrust_prop
			}
			try:
				response = getattr(user, trade_cmd['action'])(**args)
			except exceptions.TradeError as e:
				trader_name = type(user).__name__
				err_msg = '{}: {}'.format(type(e).__name__, e.args)
				log.error(
					'{} 执行 策略 [{}] 指令(股票: {} 动作: {} 数量: {} 价格: {} 指令产生时间: {}) 失败, 错误信息: {}'.
					format(trader_name, trade_cmd['strategy_name'],
						trade_cmd['stock_code'], trade_cmd['action'],
						trade_cmd['amount'], trade_cmd['price'],
						trade_cmd['datetime'], err_msg))
			else:
				log.info(
					'策略 [{}] 指令(股票: {} 动作: {} 数量: {} 价格: {} 指令产生时间: {}) 执行成功, 返回: {}'.
					format(trade_cmd['strategy_name'], trade_cmd['stock_code'],
						trade_cmd['action'], trade_cmd['amount'],
						trade_cmd['price'], trade_cmd['datetime'],
						response))
