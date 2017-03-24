from odooadapter.odoo_adapter import OdooAdapter


field_values = {
	'category_id': {
		'Sage Unit': 6,
		'Sage Barrel': 7,
	}
}

field_key_to_model = {
	'location_id': {
		'model': 'stock.location',
		'filters': 'location_id', 
		'fields': None,
		'selected_fields': 'complete_name,location_id'
	},
	'partner_id': {
		'model': 'res.partner',
		'filters': 'name',
		'fields': 'name',
		'selected_fields': 'name',
	},
	'pricelist_id': {
		'model': 'product.pricelist',
		'filters': None,
		'fields': None,
		'selected_fields': None,
	},
	'create_uid': {
		'model': 'res.users',
		'filters': 'name,login',
		'fields': None,
		'selected_fields': 'name,login',
	},
	'company_id': {
		'model': 'res.company',
		'filters': 'name',
		'fields': None,
		'selected_fields': 'name',
	},
	'journal_id': {
		'model': 'account.journal',
		'filters': 'name,code',
		'fields': None,
		'selected_fields': 'name,code',
	},
	'currency_id': {
		'model': 'res.currency',
		'filters': 'name',
		'fields': None,
		'selected_fields': 'name',
	},
	'order_line': {
		'model': 'purchase.order.line',
		'filters': 'product_id',
		'selected_fields': 'invoiced,price_unit,product_id,name,date_planned,account_analytic_id,product_qty,product_uom,partner_id,payment_term_id',
		'fields': {
			'product_id': {
				'model': 'product.product',
				'filters': 'name,active',
				'fields': 'name,type,uom_id,active',
				'selected_fields': 'name,type,uom_id,active'
			},
			'product_oum': {
				'model': 'product.uom',
				'filters': 'name',
				'fields': 'name,category_id,uom_type,active,rounding',
				'selected_fields': 'name,category_id,uom_type,active,rounding',
				},
			'account_analytic_id': {
				'model': 'account.analytic.account',
				'filters': None,
				'fields': 'name,analytic_date,type,company_id',
				'selected_fields': 'name,analytic_date,type,company_id'
			},
		},
	},
	'invoice_ids': {
		'model': 'account.invoice',
		'filters': None,
		'fields': None,
		'selected_fields': None,
	}, 
	'product_id': {
		'model': 'product.product',
		'filters': 'name,active',
		'fields': 'name,type,uom_id,active',
		'selected_fields': 'name,type,uom_id,active'
	},
	'account_analytic_id': {
		'model': 'account.analytic.account',
		'filters': None,
		'fields': 'name,analytic_date,type,company_id',
		'selected_fields': 'name,analytic_date,type,company_id'
	},
	'product_uom': {
		'model': 'product.uom',
		'filters': 'name',
		'fields': 'name,category_id,uom_type,active,rouding',
		'selected_fields': 'name,category_id,uom_type,active,rounding',
	},
	'uom_id': {
		'model': 'product.uom',
		'filters': 'name',
		'fields': 'name,category_id,uom_type,active,rouding',
		'selected_fields': 'name,category_id,uom_type,active,rounding',
	},
	'category_id': {
		'model': 'product.uom.categ',
		'filters': 'name', 
		'fields': 'name',
		'selected_fields': 'name',
	},
	'payment_term_id': {
		'model': 'account.payment.term',
		'filters': 'name',
		'fields': 'name',
		'selected_fields': 'name',
	},
	'picking_type_id': {
		'model': 'stock.picking.type',
		'filters': None,
		'fields': None,
		'selected_fields':'id',
	}
}

purchase_order_model = {
	'ignore_fields': ['picking_ids', 'shipped_rate', 'invoced_rate', 'minimum_planned_date', 'invoiced', 'amount_tax', 'amount_total', 'shipment_count', 'invoice_count'],
	'many2one_fields': [],
	'many2many_fields': [],
	'one2many': [],
	'selected_fields': ['picking_type_id','date_approve','partner_id', 'currency_id', 'order_line', 'date_order', 'vessel', 'partner_ref', 'state', 'name']
}


order_line_selected_fields = ['product_id', 'name', 'date_planned', 'account_analytic_id', 'product_qty', 'product_uom']

models_with_changed_field_values = {
	'product.uom.categ': {
		'name': {
			'old_value': 'Sage Barrel',
			'new_value': 'Sage BBL',
		}
	}
}

def is_many2one_field(field):
	if  isinstance(field, list) and len(field) == 2 and isinstance(field[1], str):
		return True

	return False

def is_many2many_field(field):
	passes = True
	if  isinstance(field, list):
		# check if all elements are integers
		for item in field:
			if passes is True:
				break

			if isinstance(item, int) is not True:
				passes = False
	else:
		passes = False

	return passes

def is_one2many_field(field):
	return is_many2many_field(field)
	

def group_data_by_column_value_per_row(orders):
	print("group_data_by_column_value_per_row()")
	groups = []
	for order in orders:
		# remove the model id before grouping
		order.pop("id")
		order_groups = {'many2one': {}, 'many2many': {}, 'primitive': {}}
						
		for field in order:
			if is_many2one_field(order[field]):
				order_groups['many2one'][field] = order[field][0]

			elif is_many2many_field(order[field]):
				order_groups['many2many'][field] = order[field]

			else:
				order_groups['primitive'][field] = order[field]

		groups.append(order_groups)

	return groups

def create_field_mode_data_using_v8_data(id, model_name, field=None):
	print('create_field_mode_data_using_v8_data()')
	print("creatingModel with name = %s" %model_name)
	print("Field = %s" %field)	
	model = odooAdapter.setModel(model_name)
	model10 = odooAdapter10.setModel(model_name)

	IGNORE_FIELDS = ['create_uid', 'write_uid']

	if field_key_to_model[field]['selected_fields'] is not None:
		selected_fields = field_key_to_model[field]['selected_fields'].split(",")
		print("SelectedFields = %s" %selected_fields)
		modelData = model.getRecordsWhere([('id', '=', id)], fields=selected_fields)[0]
	else:
		modelData = model.getRecordsWhere([('id', '=', id)])[0]
		
	# strip out all relational_fields, we're still not
	# sure how deep to cascade for relational fields
	field_groupings = group_data_by_column_value_per_row([modelData])[0]
	print("felixMany2one = %s" %field_groupings['many2one'])
	finalCreateRecord = field_groupings['primitive']
	if len(field_groupings['many2one']) > 0:
		print("HeyYOu")
		record = {}
		for field in field_groupings['many2one']:
			if field in IGNORE_FIELDS:
				continue

			print("(field  <=> value) => (%s, %s)" %(field, modelData[field]))
			modelId = model_data_exists_on_v10(field, modelData)
			print("modelId => %s" %modelId)

			if modelId is False:	
				print("modeId does not exist we create gain")
				fieldModelName = field_key_to_model[field]['model']
				print("FieldModelName = %s" %fieldModelName)
				fieldModel = odooAdapter.setModel(fieldModelName)
				fieldModel10 = odooAdapter10.setModel(fieldModelName)
				fieldModelId = field_groupings['many2one'][field]
				print("fieldModelId = %s" %fieldModelId)
				if field_key_to_model[field]['selected_fields'] is not None:
					selected_fields = field_key_to_model[field]['selected_fields'].split(",")
				else:
					selected_fields = []
				print("fieldSelectedFields = %s" %selected_fields)

				if len(selected_fields) > 0:
					fieldModelData = fieldModel.getRecordsWhere([('id', '=', fieldModelId)], fields=selected_fields)[0]
				else:
					fieldModelData = fieldModelName.getRecordsWhere([('id', '=', fieldModelId)])[0]
					fieldModelData = fieldModelData.drop('id')
				print("fieldModelData = %s" %fieldModelData)
				print("fieldModelCreate:")
				modelId = fieldModel10.createRecord(fieldModelData)
				record[field] = modelId
				print("Model not existing, let's create one")
				print("createModel ID for field %s is %s" %(field, modelId))
			else:
				print("fieldModelAlreadyExists ID:  %s" %modelId)
				print("myFieldWorld = %s" %field)
				record[field] = modelId

		finalCreateRecord.update(record)

		print("finalCreatedRecord = %s" %finalCreateRecord)
		createdItemId = odooAdapter10.setModel(model_name).createRecord(finalCreateRecord)
		print("createItemId for model (%s) = %s" %(model_name,createdItemId))

	
		return createdItemId


def model_data_exists_on_v10(field, data):
	print("model_data_exists_on_v1()")
	if field in field_key_to_model:
		modelName = field_key_to_model[field]['model']

		print("modelName = %s" %modelName)
		model = odooAdapter.setModel(modelName)
		model10 = odooAdapter10.setModel(modelName)
		if field_key_to_model[field]['filters'] is not None:
			filter = field_key_to_model[field]['filters'].split(",")
		else:
			filter = []
		
		if isinstance(data[field], list):
			fieldId = data[field][0]
		else:
			fieldId = data[field]

		print("fieldId = %s" %data[field])
		print("filter = %s" %filter)
		print("modelName = %s" %modelName)
		print("(field, value) = (%s, %s)" %(field, data[field]))
		print("selectedFields = %s" %field_key_to_model[field]['selected_fields'])
		if field_key_to_model[field]['selected_fields'] is not None:
			print('selected field != None')
			selected_fields = field_key_to_model[field]['selected_fields'].split(",")
			modelData = model.getRecordsWhere(filter=[('id', '=', fieldId)], fields=selected_fields)[0]
		else:
			print('selected fields == None ')
			modelData = model.getRecordsWhere(filter=[('id', '=', fieldId)])[0]
			selected_fields = []
		print("modelData = %s" %modelData)
			
		# change the value of all fields which has change from v8 to v10
		# E.g: field name with value 'Sage Barrel' has changed to 'Sage BBL'
		if modelName in models_with_changed_field_values:
			print("MODELS WITH CHANGE FIELD VALUES")
			print("================================")
			print("models_with_changed_fielc_values = %s" %models_with_changed_field_values)
			print("==============================================")
			print("PRODUCT.UOM.CATEG")
			print("==============================================")
			changedFilterFields = models_with_changed_field_values[modelName]
			print("changedFilterFields = %s" %changedFilterFields)
			for filter_field in filter:
				if filter_field in changedFilterFields:
					old_value = changedFilterFields[filter_field]['old_value']
					new_value = changedFilterFields[filter_field]['new_value']
					print("YES field: %s in changes" %field)
					print("field old_value = %s" %old_value)
					print("field new_value = %s" %new_value)
					if modelData[filter_field] == old_value:
						print("setting new field value")
						modelData[filter_field] = new_value

		filterClause = generate_filter_clause(filter, modelData)
		print("Filterclause = %s" %filterClause)
		if filterClause:
			modelData10 = model10.getRecordsWhere(filter=filterClause, fields=['id'])

			if len(modelData10) > 0:
				return modelData10[0]['id'] # return only the first record
			else:
				return False
		else:
			# print("modelData = %s" %modelData)
			if modelName == "stock.picking.type":
				print("//////////////////////")
				print("picking type world with id = %s" %modelData['id'])
				print("/////////////////////////")
				picking_type_id = modelData['id']
				if picking_type_id == 41 or picking_type_id == 31: #anokyi
					modelId  = 27
				elif picking_type_id == 46: # tema asogli
					modelId =  27

				elif picking_type_id == 41: #GNGC
					modelId =  27 
				return modelId
			else:
				return False

def model_data_exists_on_v10_many2many(field, id):
	print("================")
	print("model_data_exists_on_v10_many2many")
	print("===============")
	if field in field_key_to_model:
		modelName = field_key_to_model[field]['model']
		filters = field_key_to_model[field]['filters']
		model = odooAdapter.setModel(modelName)
		model10 = odooAdapter10.setModel(modelName)

		modelData = model.getRecordsWithIds(id)[0]
		filterClause = generate_filter_clause(filters, modelData)
		print("FilterClause = %s" %filterClause)
		if filterClause:
			modelData10 = model10.getRecordsWhere(filter=filterClause)
			print("ModelData10 = %s" %modelData10)
			if len(modelData10) > 0:
				return modelData10[0]
			else:
				return False
		else:
			print("no filter found, hence we did no check on v10")	
			return False


def generate_filter_clause(filter_names, data):
	print("generate_filter_clause()")
	print("filters = %s" %filter_names)
	print("filterData = %s" %data)
	if filter_names is []:
		return False
	else:
		filterClause = []
		if isinstance(filter_names, list):
			for name in filter_names:
				if isinstance(data[name], list):
					filterClause.append((name, '=', data[name][0]))
				else:
					filterClause.append((name, '=', data[name]))
		else:
			if isinstance(data[filter_names], list):
				filterClause.append((filter_names, '=', data[filter_names][0]))
			else:
				filterClause.append((filter_names, '=', data[filter_names]))
		return filterClause


def create_or_get_many2one_orders(order):
	print("create_or_get_many2one_orders()")
	print("many2one model creation = %s" %order)
	record = {}
	
	for field in order:
		print("\n\nField: %s" %field)
		modelName = field_key_to_model[field]['model']
		if modelName == "res.users":
			continue
					
		modelData = model_data_exists_on_v10(field, order) # this method returns the ID of the model if it already exist on v10 
		
		if not modelData:
			print("not existing, so we create new one")
			modelId = create_field_mode_data_using_v8_data(order[field], field_key_to_model[field]['model'], field=field)
		else:
			modelId = modelData['id']
			print("exist so we don't create again ID")
		print("createdModelID = %s" %modelId)
		record[field] = modelId 
		print("\n\n")
	
	return record

def create_or_retrieve_id_many2many_orders(order):
	print("create_or_retrieve_id_many2many_orders()")
	print("many2many model creation = %s" %order)
	record = {}
	for field in order:
		record[field] = []
		print("Field: %s" %field)
		modelName = field_key_to_model[field]['model']
		model = odooAdapter.setModel(modelName)
		model10 = odooAdapter10.setModel(modelName)

		for id in order[field]	:
			modelData10 = model_data_exists_on_v10_many2many(field, id) # this method returns the ID of the model if it already exist on v10 
			print("Hello there = %s" %modelData10)
			print("------------------------------------------")
			if not modelData10:
				selected_fields = field_key_to_model[field]['selected_fields'].split(",")
				print("modelID = %s" %id)
				print("selected fields = %s"%selected_fields)
				print("not existing, so we create new one")
				modelData10 = model.getRecordsWhere(filter=[('id', '=', id)], fields=selected_fields)
				print("modelDataFrom8 = %s" %modelData10)
				mappings = group_data_by_column_value_per_row(modelData10)
				# Before we go ahead to create model, we need to figure out if they are any field object that have  been specified, as needing creation
				fields = field_key_to_model[field]['fields']
				print("inner fields are %s\n" %(fields))
				print("mappings is %s\n" %mappings)
				if fields is not None:
					if len(mappings['many2many']) > 0:
						print("fields are %s" %fields)
						for key in fields:
							print("key = %s" %key)
							if key in mappings['many2many']:
								# get a record with the ID 
								print("field %s value is %s" %(key, mappings['many2many'][key]))
							else:
								print("many2many key does not exist")
								# create_or_get_many2one_orders(model.getRecordsWithIds(mappings['many2many'][key]))


					# let check if we auth to create field_object data
					
					if len(mappings['many2one']) > 0:
						print("many2one mapping > 0")
						many2one = mappings['many2one'][0]
						data = {}
						for key in fields:
							print('many2one key is %s' %key)
							if key in many2one:
								print("field %s value is %s(many2one)\n" %(key, many2one[key]))
								data[key] = many2one[key]
							else:
								print('many2one key does not exist')

						if len(data) > 0:
							print("understanding = %s" %data)
							# create_or_get_many2one_orders(data)

				print("mappings = %s" %mappings)
			else:
				modelId10 = modelData10['id']
				print("exists with ID = %s" %modelId10)
				record[field].append(modelId10)

		print("record is %s" %record)
		return record


def get_fields_id_from_v10(order_fields):
	print("\nget_fields_id_from_v10()")
	print("Fields = %s" %order_fields)
	record = {}
	for field in order_fields:
		print("\n\nField: %s" %field)
		modelId = model_data_exists_on_v10(field, order_fields) # this method returns the ID of the model if it already exist on v10 
		if modelId is False:
			print("not existing, so we create new one")
			modelId = create_field_mode_data_using_v8_data(order_fields[field], field_key_to_model[field]['model'], field=field)
			print("createdID = %s " %modelId)
		else:
			print("FieldInside = %s" %field)
			print("existID = %s" %modelId)
		record[field] = modelId 
	return record


def get_fields_id_from_v10_for_many2many(order, orderId=None):
	print("\n\n")
	print("get_fields_id_from_v10_for_many2many()")
	print("many2many model creation = %s" %order)
	print("OrderId = %s" %orderId)
	record = {}
	for field in order:
		print("====================>>>")
		print("\n\nField: %s" %field)
		print("====================>>>")
		modelName = field_key_to_model[field]['model']
		print("modelNameHey = %s" %modelName)
		model = odooAdapter.setModel(modelName)
		model10 = odooAdapter10.setModel(modelName)

		record[field] = [] # holder for the created or retrieved ID's of field
		for id in order[field]	:
			modelId10 = model_data_exists_on_v10_many2many(field, id) # this method returns the ID of the model if it already exist on v10 
			print("modelId10 = %s" %modelId10)
			print("---------------------")
			if not modelId10:
				selected_fields = field_key_to_model[field]['selected_fields'].split(",")
				print("modelID = %s" %id)
				print("selectedFields = %s"%selected_fields)
				print("not existing, so we create new one")
				modelData10 = model.getRecordsWhere(filter=[('id', '=', id)], fields=selected_fields)
				print("modelDataFrom8 = %s" %modelData10)
				mappings = group_data_by_column_value_per_row(modelData10)
				mappings = mappings[0]
				# Before we go ahead to create model, we need to figure out if they are any field object that have  been specified, as needing creation
				fields = field_key_to_model[field]['fields']
				print("innerFields =  %s\n" %(fields))
				print("mappings = %s\n" %mappings)
				print("primitive = %s" %mappings['primitive'])
				# get_fields_id_from_v10(mappings['many2one'])
				print("fields = %s" %fields)
				# if len(mappings['many2many']) > 0:
				# 	print("Fields = %s" %fields)
				# 	for key in fields:
				# 		print("key = %s" %key)
				# 		if key in mappings['many2many']:
				# 			# get a record with the ID 
				# 			print("(field, value) = (%s, %s)" %(key, mappings['many2many'][key]))
				# 		else:
				# 			print("many2many key does not exist")
				# 			# create_or_get_many2one_orders(model.getRecordsWithIds(mappings['many2many'][key]))


				# let check if we auth to create field_object data
				print("many2oneLength  = %s" %len(mappings['many2one']))
				if len(mappings['many2one']) > 0:
					print("many2one mapping > 0")
					print("many2one = %s" %mappings['many2one'])
					result = get_fields_id_from_v10(mappings['many2one'])
					print("Hello Result = %s" %result)
					mappings['primitive'].update(result)
					mappings['primitive'].update({"order_id": orderId})
				print("myPrimitive = %s" %mappings['primitive'])
				record[field].append(mappings['primitive'])
			else:
				# model already exists, so let use it's v10 ID
				print("exists with ID = %s" %modelId10)
				record[field].append(modelId10)
	print("Record = %s" %record)	
	return record


def migrate_purchase_orders(orders):
	orders_groupings = group_data_by_column_value_per_row(orders)
	# print("groupings = %s" %orders_groupings[0])
	"""
		1. Get many2one fields
		2. Check v10 if it exists there, if yes, get the fields ID, else, we create it from v8's data
		3. add {key: fieldId} to fieldsBag = {}
		4. Create purchase.order with fieldsBag
		5. Now that purchase.order is created, we will update 'order_id' in order_lines which has it's 'id' in 'order_line'
	"""
	ordersLines = []
	createdOrders = []
	createdOrdersIds = []
	index = 0
	for order_groups in orders_groupings:
		print("==================>>")
		print("\n\nCreating order")
		print("==================>>")
		# if index == 1:
		# 	break
		createdOrder = {}
		record = order_groups['primitive']
		many2one_fields = order_groups['many2one']
		many2many_fields = order_groups['many2many']

		ordersLines.append(many2many_fields)
		many2one_field_record = get_fields_id_from_v10(many2one_fields)
		record.update(many2one_field_record)
		# Change 'state' field value to 'draft'
		record.pop('state')
		record.update({'state': 'draft'})

		orderId = odooAdapter10.setModel('purchase.order').createRecord(record)
		createdOrder['order_id'] = orderId
		createdOrdersIds.append(orderId)
		orderLine = get_fields_id_from_v10_for_many2many(many2many_fields, orderId)['order_line']
		print("orderLine = %s" %orderLine)
		createdOrder['order_line_ids'] = []
		for line in orderLine:
			line.update({"order_id":orderId})
			createdOrderLineId = odooAdapter10.setModel('purchase.order.line').createRecord(line)
			createdOrder['order_line_ids'].append(createdOrderLineId)

		createdOrders.append(createdOrders)
		index += 1

		# Time to confirm all orders
		# order = confirm_response = objectInstance['purchase.order'].browse(orderId)
		# print("MYORDEr = %s" %order)
		# confirm_response = order.button_confirm()
		# print("\nConfirming order with ID = %s" %orderId)
		# print("-----------------------------------------")
		# print("Confirm order response = %s" %confirm_response)

	return createdOrdersIds



def migrate_orders(orders, migration_details=None):
	print("Starting migrations")
	print("Total Orders = %s" %len(orders))
	print("migraiont detaisl = %s" %migration_details)

	global odooAdapter
	global odooAdapter10
	global objectInstance
	config = migration_details['from']
	config10 = migration_details['to']
	order_date = migration_details['order_date']
	objectInstance = migration_details['object_instance']
	is_migrate_purchase_orders = migration_details['migrate_purchase_orders']
	is_migrate_sale_orders = migration_details['migrate_sale_orders']

	global PurchaseOrder
	global PurchaseOrderLine
	PurchaseOrder = objectInstance.env['purchase.order']
	PurchaseOrderLine = objectInstance.env['purchase.order.line']

	odooAdapter = OdooAdapter().setServerConfig(config).authenticate()
	odooAdapter10 = OdooAdapter().setServerConfig(config10).authenticate()
	print("Date ORDER = %s" %order_date)
	orders = odooAdapter.setModel('purchase.order').getRecordsWhere(filter=[('date_order', ">=", order_date), ('date_order', '<=', order_date), ('state', '=', 'done')], fields=purchase_order_model['selected_fields'])
	createdOrdersIds = migrate_purchase_orders(orders)
	
	return createdOrdersIds


