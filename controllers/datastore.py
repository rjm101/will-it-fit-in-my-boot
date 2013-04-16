from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from google.appengine.ext import db
from google.appengine.api.datastore import Key
from google.appengine.api import memcache
import itertools
import logging
import os
import time
import cgi
import datetime

# Import local scripts
from models import models


def get_navigation(**kwargs):
	response = None
	try:
		memcache_key = create_memcache_key('navigation', **kwargs)
		memcache_result = memcache.get(memcache_key)
		if memcache_result is not None:
			response = memcache_result
		else:			
			navigation = dict()
			department_query = models.Department.all()
			department_query = department_query.fetch(limit=None)
			for dept in department_query:
				navigation[dept.name] = [c.name for c in dept.categories.fetch(limit=None)]

			response = navigation
			memcache.set(memcache_key, value=response)
	except Exception, e:
		raise e
	finally:
		return response

"""
	@name: get_departments
	@description:
		Return all Departments, with each Department as the Display Name Key for a list of Categories
"""
def get_departments(**kwargs):
	response = None
	limit = 50
	try:
		memcache_key = create_memcache_key('department', **kwargs)
		memcache_result = memcache.get(memcache_key)
		if memcache_result is not None:
			response = memcache_result
		else:
			# Query all Departments
			query = models.Department.all()

			# Attempt to get a kwargs limit
			try:
				if 'limit' in kwargs and kwargs['limit'] != '':
					limit = int(kwargs['limit'])
			except Exception, e:
				logging.error(e)

			# Fetch the categories from the Query. Always returns a list, even an empty one
			response = query.fetch(limit=limit)

			# Only attempt to turn the departments into a list of dict objects if there are any
			if len(response) > 0:
				response = [d.to_dict() for d in response]
				
			# Store the result in Memcache even if there are no departments, so we have cached the query
			memcache.set(memcache_key, value=response)
			
	except Exception, e:
		raise e
	finally:
		return response
"""
	@name: get_categories
	@description:
		Return all available Categories that match any kwargs
	@returns:
		list of Category Models in dict, or an empty list
"""
def get_categories(**kwargs):
	response = None
	limit = 50
	try:
		memcache_key = create_memcache_key('category', **kwargs)
		memcache_result = memcache.get(memcache_key)
		if memcache_result is not None:
			response = memcache_result
		else:
			# Query all Categories
			query = models.Category.all()

			# Attempt to get a kwargs limit
			try:
				if 'limit' in kwargs and kwargs['limit'] != '':
					limit = int(kwargs['limit'])
			except Exception, e:
				logging.error(e)

			# Fetch the categories from the Query. Always returns a list, even an empty one
			response = query.fetch(limit=limit)

			# Only attempt to turn the categories into a list of dict objects if there are any
			if len(response) > 0:
				response = [c.to_dict() for c in response]
				
			# Store the result in Memcache even if there are no categories, so we have cached the query
			memcache.set(memcache_key, value=response)

		return response
	except Exception, e:
		logging.error(e)
		raise e

"""
	@name: get_products
	@description:
		Return all available Products that match any kwargs
	@returns:
		list of Product Models in dict format, or an empty list
"""
def get_products(**kwargs):
	response = None
	query = None
	# Force the default limit for product to be 25, so we don't start querying for thousands of them
	limit = 25
	try:
		memcache_key = create_memcache_key('products', **kwargs)
		memcache_result = memcache.get(memcache_key)
		if memcache_result is not None:
			response = memcache_result
		else:
			
			# Check initially whether to look up the Category to filter products from there
			if 'category' in kwargs and kwargs['category'] != '':
				category = models.Category.get_by_key_name(kwargs['category'])
				if category is not None:
					query = category.products
				else:
					raise Exception('No category exists with the key_name '+kwargs['category'])				
			# Or, to look up all Products
			else:
				query = models.Product.all()

			# Filter by Department
			if 'department' in kwargs and kwargs['department'] != '':
				query.filter('department = ', kwargs['department'])

			# Filter by type
			if 'type' in kwargs and kwargs['type'] != '':
				query.filter('type = ', kwargs['type'])

			# Filter by colour
			if 'colour' in kwargs and kwargs['colour'] != '':
				query.filter('colour = ', kwargs['colour'])

			# Filter by collection
			if 'collection' in kwargs and kwargs['collection'] != '':
				query.filter('collection = ', kwargs['collection'])

			# Filter by priceMin
			if 'priceMin' in kwargs and kwargs['priceMin'] != '':
				price_min = float(kwargs['priceMin'])
				query.filter('price >= ',  price_min)

			# Filter by priceMax
			if 'priceMax' in kwargs and kwargs['priceMax'] != '':
				price_max = float(kwargs['priceMax'])
				query.filter('price <= ',  price_max)

			
			# Filter by Dimension Width.
			# Always filter less than or equal to, thus maxWidth
			if 'width' in kwargs and kwargs['width'] != '':
				width = float(kwargs['width'])
				def filter_by_width(a):
					if a.width is not None and a.width <= width:
						return True
					else:
						return False
				query = filter(filter_by_width, query)
			
			# Filter by Dimension Height.
			# Always filter less than or equal to, thus maxHeight
			if 'height' in kwargs and kwargs['height'] != '':
				height = float(kwargs['height'])
				def filter_by_height(a):
					if a.height is not None and a.height <= height:
						return True
					else:
						return False
				query = filter(filter_by_height, query)
			
			# Filter by Dimension Depth.
			# Always filter less than or equal to, thus maxDepth
			if 'depth' in kwargs and kwargs['depth'] != '':
				depth = float(kwargs['depth'])
				def filter_by_depth(a):
					if a.depth is not None and a.depth <= depth:
						return True
					else:
						return False
				query = filter(filter_by_depth, query)				

			# Filter by Dimension Length.
			# Always filter less than or equal to, thus maxLength
			if 'length' in kwargs and kwargs['length'] != '':
				length = float(kwargs['length'])
				def filter_by_length(a):
					if a.length is not None and a.length <= length:
						return True
					else:
						return False
				query = filter(filter_by_length, query)
				

			# Order by price as default??
			# query.order('price')
			# Cannot use for all query params due to first ordering property 'feature' of GAE
			# Use sorted() method instead

			# Attempt to get a kwargs limit. Only log the error do not raise it, and we will keep our default limit intact
			try:
				if 'limit' in kwargs and kwargs['limit'] != '':
					limit = int(kwargs['limit'])
			except Exception, e:
				logging.error(e)
			
			# Fetch the products from the Query. Always returns a list, even an empty one
			if isinstance(query, db.Query):
				response = query.fetch(limit=limit)
			else:
				response = query[:limit]

			# Only attempt to turn the products into a list of dict objects if there are any
			if len(response) > 0:
				response = [p.to_dict() for p in response]
				
			# Store the result in Memcache even if there are no products, so we have cached the query
			memcache.set(memcache_key, value=response)
			
		return response
	except Exception, e:
		logging.error(e)
		raise e


"""
	@name: create_memcache_key
	@description:
		Create and return a Memcache Key using a prefex and kwargs
"""
def create_memcache_key(key_prefix, **kwargs):
	memcache_key = key_prefix+':'
	if kwargs is not None:
		for request_arg, value in kwargs.items():
			if type(value) == list or type(value) == int:
				value = str(value)
			memcache_key+=request_arg+'='+value

	return memcache_key