# -*- coding: utf-8 -*-

from odoo import models, fields, api

from ..migration_script import migrate
from ..migration_script.odooadapter.odoo_adapter import OdooAdapter

class qg_albert(models.Model):
    _name = 'qg_albert.qg_albert'

    def get_current_system_time(self):
    	print("field Date = %s" %fields.Date.today())
    	return fields.Date.today()

    date = fields.Date(required=True, default=get_current_system_time, readonly=True)
    purchase_order_process = fields.Boolean("PO Process", required=True, default=True)
    sale_order_process = fields.Boolean("SO Process", required=True, default=True)

    def confirm_purchase_orders(self, orders):
    	response = self.env['purchase.order'].browse(orders).button_confirm()
    	return response


    def migrate_orders(self):
    	print("migration orders")
    	print("purchase order = %s" %self.purchase_order_process)
    	print("sale order = %s" %self.sale_order_process)

    	# config10 = {
    	# 	'username': 'erpadmin',
    	# 	'password': '123',
    	# 	'database': 'odoo_purchase_prod2',
    	# 	'url': 'http://127.0.0.1:8071'
    	# }

    	# config = {
    	# 	'username': 'erpadmin',
    	# 	'password': '123',
    	# 	'database': 'purchases',
    	# 	'url': 'http://127.0.0.1:8069'
    	# }

    	# odooAdapter10 = OdooAdapter().setServerConfig(config10).authenticate()
    	# odooAdapter = OdooAdapter().setServerConfig(config).authenticate()
    	migration_details = {
    		'from': {
    			'username': 'erpadmin',
    			'password': '123',
    			'database': 'purchases',
    			'url': 'http://127.0.0.1:8069',
    		},
    		'to': {
    			'username': 'erpadmin',
    			'password': '123',
    			'database': 'odoo_purchase_prod2',
    			'url': 'http://127.0.0.1:8071',
    		},
    		'object_instance':self,
    		'order_date': self.date,
    		'migrate_purchase_orders': self.purchase_order_process,
    		'migrate_sale_orders': self.sale_order_process,
    	}

    	createdOrderIds = migrate.migrate_orders([], migration_details=migration_details)
    	print("Created Order Ids = %s" %createdOrderIds)
    	import time
    	time.sleep(10)
    	for order in self.env['purchase.order'].browse(createdOrderIds):
    		print("order = %s" %order)
    		response = order.button_confirm()
    		print("reson = %s" %response)
    	# orders = self.env['purchase.order'].browse(createdOrderIds)
    	# print("orders = %s" %orders)
    	# response = orders.button_confirm()
    	# print("response = %s" %response)