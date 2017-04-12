
def get_orders(objectInstance):
	result = objectInstance.env['purchase.order'].search([])
	print("get_orders result = %s" %result)
	print("get_odrer result length = %s" %len(result))
	print("----------------------")
	query = "SELECT count(*) FROM purchase_order"
	result = objectInstance.env.cr.execute(query)
	print("Hey", objectInstance.env.cr.fetchall())
	print("Query Result = %s" %result)