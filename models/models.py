# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

from ..migration_script import migrate
from ..migration_script.odooadapter.odoo_adapter import OdooAdapter


class PurchaseOrderHistory(models.Model):

    _name = "qg_albert.order_history"

    date = fields.Date()
    name = fields.Char()
    order_type = fields.Integer()
    order_placed = fields.Boolean(default=False)
    order_confirmed = fields.Boolean(default=False)
    order_received = fields.Boolean(default=False)


ORDER_STATES = {
	'placed': 'placed',
	'confirmed': 'confirmed',
	'received': 'received',
}


class qg_albert(models.Model):
    _name = 'qg_albert.qg_albert'

    PURCHASE_ORDER = 1
    SALE_ORDER = 2

    createdOrderNames = []


    def get_current_system_time(self):
        return fields.Date.today()

    def migration_details(self):
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
            'object_instance': self,
            'order_date': self.date,
            'run_purchase_orders_migration': self.purchase_order_process,
            'run_sale_orders_migration': self.sale_order_process,
        }

        return migration_details


    date = fields.Date(required=True, default=get_current_system_time)
    purchase_order_process = fields.Boolean("PO Process", required=True, default=True)
    sale_order_process = fields.Boolean("SO Process", required=True, default=True)
    state = fields.Selection([('mig_po','Migr_ordersate PO'),('conf_po','Confirm PO'),('recv_po','Receive PO'),('mig_so','Migrate SO'),('conf_so','Confirm SO'),('recv_so','Receive SO'),('done','Done')],string="Stage",default='mig_po')

    def process_state(self):
        if self.state in ('mig_po','conf_po','recv_po'):
            self.purchase_order_process=True
            self.sale_order_process=False
        else:
            self.purchase_order_process=False
            self.sale_order_process=True

        if self.state == 'mig_po':
            self.migrate_orders()
            self.state='conf_po'
        elif self.state == 'conf_po':
            self.confirm_orders()
            self.state='recv_po'
        elif self.state == 'recv_po':
            self.receive_orders()
            self.state='mig_so'
        elif self.state == 'mig_so':
            self.migrate_orders()
            self.state='conf_so'
        elif self.state == 'conf_so':
            self.confirm_orders()
            self.state='recv_so'
        elif self.state == 'recv_so':
            self.receive_orders()
            self.state = 'done'


    # def confirm_purchase_orders(self, orders):
    #     response = self.env['purchase.order'].browse(orders).button_confirm()

    #     return response

    def confirm_orders(self):
        print("confirm_orders()")

        if self.purchase_order_process:
            orders  = self.env['purchase.order'].search([('date_order', ">=", self.date), ('date_order', '<=', self.date)])
            print("orders = %s" %orders)
            orderNames = []
            for order in orders:
                order.button_confirm()
                orderNames.append(order.name)

            if len(orderNames) > 0:
            	print("purchase order names = %s" %orderNames)
            	self.save_order_names(orderNames, self.PURCHASE_ORDER, ORDER_STATES['confirmed'])

        if self.sale_order_process:
            orders  = self.env['sale.order'].search([('date_order', ">=", self.date), ('date_order', '<=', self.date)])
            print("sales order names = %s" %orders)
            orderNames = []
            for order in orders:
                order.action_confirm()
                orderNames.append(order.name)

            if len(orderNames) > 0:
                print("sales order names = %s" %orderNames)
                self.save_order_names(orderNames, self.SALE_ORDER, ORDER_STATES['confirmed'])


    def receive_orders(self):
    	print("recieve_orders()")
    	if self.purchase_order_process:
            orders = self.env['purchase.order'].search([('date_order', '>=', self.date), ('date_order', '<=', self.date)])
            print("orders = %s" %orders)

            orderNames = []
            for order in orders:
                orderNames.append(order.name)
            print("orderNames = %s" %orderNames)

            migrate.migrate_stock_pickings(orderNames, self.migration_details())
            for order in orders:
                picking_ids = order.picking_ids.ids
                print("picking_ids = %s" %picking_ids)
                for id in picking_ids:
                    env = api.Environment(self.env.cr, self.env.uid, {'active_ids': [id]})
                    stockPicking = env['stock.immediate.transfer'].create({"pick_id": id})
                    
                    print("created StockPicking = %s" %stockPicking)
                    stockPicking.process()
            
            self.save_order_names(orderNames, self.PURCHASE_ORDER, ORDER_STATES['received'])

        if self.sale_order_process:
            orders = self.env['sale.order'].search([('date_order', '>=', self.date), ('date_order', '<=', self.date)])
            print("orders = %s" %orders)

            orderNames = []
            for order in orders:
                orderNames.append(order.name)
            print("orderNames = %s" %orderNames)

            migrate.migrate_stock_pickings(orderNames, self.migration_details())
            for order in orders:
                picking_ids = order.picking_ids.ids
                print("picking_ids = %s" %picking_ids)
                for id in picking_ids:
                    env = api.Environment(self.env.cr, self.env.uid, {'active_ids': [id]})
                    stockPicking = env['stock.immediate.transfer'].create({"pick_id": id})
                    
                    print("created StockPicking = %s" %stockPicking)
                    stockPicking.process()
            
            self.save_order_names(orderNames, self.SALE_ORDER, ORDER_STATES['received'])






    def save_order_names(self, order_names, order_type, order_state=None):

    	if len(order_names) == 0:
    		return False

    	if order_state == ORDER_STATES['placed']:
    		history = {'date': self.date, 'order_type': order_type, 'order_placed': True}
	        for name in order_names:
	        	history['name'] = name
	        	saved = self.env['qg_albert.order_history'].create(history)
	        	print("saved = %s" %saved)
    	elif order_state == ORDER_STATES['confirmed']:
        	history = self.env['qg_albert.order_history'].search([('name', 'in', order_names), ('date', '=', self.date), ('order_placed', '=', True)])
        	history.update({"order_confirmed": True})
        elif order_state == ORDER_STATES['received']:
        	history = self.env['qg_albert.order_history'].search([('name', 'in', order_names), ('date', '=', self.date), ('order_placed', '=', True), ('order_confirmed', '=', True)])
    		history.update({"order_received": True})
    	else:
    		raise Exception("We can not save order naems without an order state provied")



    def is_order_placed(self, order_name, order_type):
        print("is_order_placed() with params = %s, %s" %(order_name, order_type))
        if order_type == self.PURCHASE_ORDER:
            count = self.env['qg_albert.order_history'].search_count([('name', '=', order_name), ('order_type', '=', self.PURCHASE_ORDER), ('order_placed', '=', True)])
            print("orderPlacedCount = %s" %count)
            if count == 1:
                return True

            return False

        elif order_type == self.SALE_ORDER:
            count = self.env['qg_albert.order_history'].search_count([('name', '=', order_name), ('order_type', '=', self.SALE_ORDER), ('order_placed', '=', True)])
            print("orderPlacedCount = %s" %count)
            if count == 1:
                return True

            return False

        else:
            raise Exception("Can process without an order type(eitehr PURCHASE_ORDER OR SALE_ORDER")


    def is_order_confirmed(self, order_name, order_type):
        if order_type == self.PURCHASE_ORDER:
            count = self.env['qg_albert.order_history'].search_count([('name', '=', order_name), ('order_type', '=', self.PURCHASE_ORDER), ('order_confirmed', '=', True)])
            if count == 1:
                return True

            return False

    def is_order_received(self, order_name, order_type):
        if order_type == self.PURCHASE_ORDER:
            count = self.env['qg_albert.order_history'].search_count([('name', '=', order_name), ('order_type', '=', self.PURCHASE_ORDER), ('order_placed', '=', True), ('order_confirmed', '=', True), ('order_received', '=', True)])
            if count == 1:
                return True

            return False

    def migrate_orders(self):
        print("migration orders")
        createdOrderNames = migrate.migrate_orders([], migration_details=self.migration_details())
        print("----------------------")
        print("createdOrderNames == %s" %createdOrderNames)
        purchaseOrderNames = createdOrderNames['purchases']
        saleOrderNames = createdOrderNames['sales']

        if len(purchaseOrderNames) > 0:
            print("Saving purchases orders placed in history len(names) = %s" %len(purchaseOrderNames))
            self.save_order_names(purchaseOrderNames, order_type=self.PURCHASE_ORDER, order_state=ORDER_STATES['placed'])

        else:
            print("Not purchase names to save")


        if len(saleOrderNames) > 0:
            print("Saving sales orders placed in history len(names) = %s" %len(saleOrderNames))
            self.save_order_names(saleOrderNames, order_type=self.SALE_ORDER, order_state=ORDER_STATES['placed'])
        else:
            print("No sales names tos save")




