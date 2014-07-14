'''
Created on Nov 21, 2012

@author: Zhixing
'''

from google.appengine.ext import db
from google.appengine.api import memcache

import logging

class ModelController:
	class Order:
		Asc, Desc = range(2)
		
	mc = memcache.Client()
	
	@classmethod
	def object_parent(cls, db_model, group="default"):
		return db.Key.from_path(db_model.kind(), group)

	@classmethod
	def object_by_id(cls, db_model, oid, parent=None):
		mc_key = db_model.kind() + str(oid)
		r = cls.mc.get(mc_key)
		if r is None:
			logging.warning('DB QUERY: ' + db_model.kind() + ' ' + str(oid))
			if parent is None:
				parent = cls.object_parent(db_model)
			r = db_model.get_by_id(int(oid), parent)
			if r:
				cls.mc.set(mc_key, r)
		return r
	
#	@classmethod
#	def object_by_attr(cls,db_model,attr,parent=None):
#		mc_key = db_model.kind() + str(attr)
#		r = cls.mc.get(mc_key)
#		if r is None:
#			logging.warn('DB QUERY: ' + db_model.kind() + ' ' + str(attr))
#			if parent is None:
#				parent = cls.object_parent(db_model)
#			r = db_model.get_by_attr(attr, parent)
#			if r:
#				cls.mc.set(mc_key, r)
#		return r

	@classmethod
	def add_object(cls, db_object):			
		db_object.put()
		oid = str(db_object.key().id())
		mc_key = db_object.kind() + oid
		cls.mc.set(mc_key, db_object)
		return oid
	
	@classmethod
	def list_mc_key(cls, parent_obj, db_model, order_key=None, limit=None):
		if parent_obj:
			mc_key = parent_obj.kind() + str(parent_obj.key().id())
		mc_key += db_model.kind()
		if order_key:
			mc_key += '|' + order_key
		if limit:
			mc_key += '|' + limit
		return mc_key
	
	@classmethod
	def get_origin_key(cls, order_key=None):
		logging.warning('order_key = ' + str(order_key))
		if not order_key:
			return None, None
		if order_key.startswith('-'):
			return cls.Order.Desc, order_key[1:]
		else:
			return cls.Order.Asc, order_key
			
	@classmethod
	def get_mc_list(cls, parent_obj, db_model,
					order_key=None, limit=None, collection_name=None, force_read=False):
		mc_key = cls.list_mc_key(parent_obj, db_model, order_key, limit)
		model_list = cls.mc.get(mc_key)
		from_db = False
		if (model_list is None) or force_read:
			if not collection_name:
				collection_name = db_model.default_collection
			warning_info = 'DB QUERY: ' + collection_name
			
			if parent_obj:
				list_query = getattr(parent_obj, collection_name)
				warning_info += ' for ' + parent_obj.kind() + ' ' + str(parent_obj.key().id())
			else:
				list_query = db_model.all()
			
			logging.warning(warning_info)
			order, origin_key = cls.get_origin_key(order_key)
			model_list = []
			if order is not None:
				list_query.order(order_key)
				for model in list_query.run(limit=limit):
					model_list.append((model.key().id(), getattr(model, origin_key)))
			else:
				for model in list_query.run(limit=limit):
					model_list.append(model.key().id())
					
			cls.mc.set(mc_key, model_list)
			from_db = True
		return mc_key, model_list, from_db
	
	@classmethod
	def update_mc_list(cls, parent_obj, update_obj, order_key=None, limit=None):
		mc_key, model_list, from_db = cls.get_mc_list(parent_obj, update_obj.__class__, order_key, limit) #@UnusedVariable
		order, origin_key = cls.get_origin_key(order_key)
		if from_db:
			return
		
		update_id = update_obj.key().id()
		if order is not None:
			logging.warning(order)
			update_item = (update_id, getattr(update_obj, origin_key))
			logging.warning("update_item" + str(update_item))
			
			insert_pos = 0
			origin_pos = -1
			for i, item in enumerate(model_list):
				logging.warning('item' + str(item))
				if item[0] == update_item[0]:	# if item's id == update_item's id
					origin_pos = i
				if ((item[1] > update_item[1]) == order):
					insert_pos = i + 1
					
			if (origin_pos >= 0) and (model_list[origin_pos][1] != update_item[1]):
				if insert_pos > origin_pos:
					insert_pos -= 1
				model_list.remove(origin_pos)
				model_list.insert(insert_pos, update_item)
			elif (origin_pos < 0):
				model_list.insert(insert_pos, update_item)
					
		elif model_list.count(update_id) == 0:
			model_list.insert(0, update_id)
			
		if limit and (len(model_list) > limit + 1):
			model_list.pop()
		
		cls.mc.set(mc_key, model_list)
		
	@classmethod
	def get_list_iter(cls, parent_obj, db_model,
					  order_key=None, limit=None, collection_name=None, force_read=False):
		mc_key, model_list, from_db = cls.get_mc_list(parent_obj, db_model, order_key, limit, collection_name, force_read) #@UnusedVariable
		order, origin_key = cls.get_origin_key(order_key) #@UnusedVariable
		logging.warning(str(order) + origin_key)
		if limit and len(model_list) > limit:
			model_list.pop()
			
		object_list = []
		if order is not None:
			for model in model_list:
				object_list.append(cls.object_by_id(db_model, model[0]))
		else:
			for model_id in model_list:
				object_list.append(cls.object_by_id(db_model, model_id))		
		return object_list
	
				
