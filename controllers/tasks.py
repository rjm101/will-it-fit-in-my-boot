import os
import logging
import datetime
import base64
import cgi
import time
import urllib
import urlparse
try:
    from urlparse import parse_qs
except ImportError: # old version, grab it from cgi
    from cgi import parse_qs
    urlparse.parse_qs = parse_qs
import cStringIO
from google.appengine.ext import db
from google.appengine.api.datastore import Key
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.ext import blobstore
from google.appengine.api import taskqueue
from google.appengine.api import mail
from google.appengine.api import urlfetch
from google.appengine.runtime import DeadlineExceededError
from google.appengine.runtime import apiproxy_errors 
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from google.appengine.ext.db import BadValueError
from google.appengine.api import images
import simplejson as json
from collections import deque
from operator import itemgetter

# Import local modules or scripts
from controllers import datastore
from models import models
from controllers import utils
from controllers import html_parser

class ProductCollection(utils.BaseHandler):
	def process(self):
		result = None
		category_key_name = ''
		try:
			department_key = str(self.request.get('department_key'))
			category_url = str(self.request.get('category_url'))
			
			response = urlfetch.fetch(url=category_url, method=self.urlfetch['method'], deadline=self.urlfetch['deadline'], headers=self.urlfetch['headers'])

			# Get available colours from Product
			colours = models.Product.properties()['colour'].choices			

			if response.status_code == 200:
				result = response.content
					
				# Parse the response content into a MiniDom object
				minidom_document = html_parser.parse_html_document(result)

				# Set the Department
				department = models.Department.get_or_insert(
					key_name=department_key, 
					name=department_key.title()
				)
				department_display_name = department.name

				# Get the Category Name form the Page H1 Header
				category_name = minidom_document.getElementsByTagName('h1')[0].childNodes[0].nodeValue
				try:
					if category_name is not None:
						category_key_name = category_name.lower().replace(' ','')
				except Exception, e:
					logging.error('Get Category')
					logging.error(e)

				# Create the Category Model
				category = models.Category.get_or_insert(
					key_name=category_key_name, 
					name=category_name, 
					department=department
				)

				# Collect all DIVs
				all_div_elements = minidom_document.getElementsByTagName('div')

				# For each DIV in the MiniDom object
				for div in all_div_elements:

					# If the DIV id is productsList, we've found the product list container
					if div.getAttribute('id') == 'productsList':
						# Get it's child DIVs
						product_list_divs = div.getElementsByTagName('div')
						# For each of those
						for div in product_list_divs:
							# If the DIV includes a class value of 'productCont' then we expect it to be a product
							if 'productCont' in div.getAttribute('class'):
								sku = None
								name = ''
								price = None
								product = div
								colour = ''
								_type = None
								collection = None
								url = None
								# Get SKU code
								try:
									sku = product.getAttribute('id')
									sku = sku.replace('id_', '')
								except Exception, e:
									logging.error('Get SKU')
									logging.error(e)
									raise Exception('No product SKU found for category_url : '+category_url)
								
								# Get Collection and Name
								try:
									for div in product.getElementsByTagName('div'):
										if 'product_info' in div.getAttribute('class'):
											spans = div.getElementsByTagName('span')
											for span in spans:
												if 'product_collection' in span.getAttribute('class'):
													collection = span.childNodes[0].nodeValue
												else:
													nodes = span.childNodes
													for node in nodes:
														name = name+node.nodeValue.strip()+' '
												
											name = name.strip()
											break											
								except Exception, e:
									logging.error('Error getting Collection and Name')
									logging.error(e)
									raise Exception('No Product Name found for category_url : '+category_url)

								# Get Product Colour
								try:
									for word in name.split(' '):
										if word in colours:
											colour = word
											break
								except Exception, e:
									logging.error('Error Getting Colour')

								# Get Product URL
								try:
									anchors = product.getElementsByTagName('a')
									if len(anchors) > 0:
										for anchor in anchors:
											if 'product_image_link' in anchor.getAttribute('class'):
												url = anchor.getAttribute('href')
												break
								except Exception, e:
									logging.error('Error Getting Product URL')

								# Get Product Price
								try:
									product_paragraphs = product.getElementsByTagName('p')
									for paragraph in product_paragraphs:
										if 'product_price' in paragraph.getAttribute('class'):
											spans = paragraph.getElementsByTagName('span')
											for span in spans:
												span_class = span.getAttribute('class')

												if 'one_price' in span_class:
													price = span.childNodes[1].nodeValue
													break
												elif 'now_price' in span_class:
													for price_span in span.getElementsByTagName('span'):
														if 'price_value' in price_span.getAttribute('class'):
															price = price_span.childNodes[1].nodeValue
															break
									if price is not None:
										price = price.replace(',','')
										price = float(price)


								except Exception, e:
									logging.error('Get Price')
									logging.error(e)
								
								# Create or Get the Product if it already exists
								product = models.Product.get_or_insert(
									key_name=sku,
									name=name,
									price=price,
									colour=colour,
									type=_type,
									category=category,
									department=department_display_name,
									collection=collection,
									url=url
								)

								# Now check for changes to Product attributes
								change = False

								# Create Images
								try:
									for key, src in self.product_template['images'].items():
										path = src.replace('@id@', sku)
										image = models.Image(
											type=key,
											url=path
										)
										image_key = image.save()
										product.images.append(image_key)
									
									change=True
								except Exception, e:
									logging.error('Get Medium Image')
									logging.error(e)
									raise Exception('No Product Medium Image found for category_url : '+category_url)
								
								if product.name != name:
									product.name = name
									change = True
								
								if product.department != department_display_name:
									product.department = department_display_name
									change = True

								if price != product.price:
									product.price=price
									change = True

								if product.colour != colour:
									product.colour = colour
									change = True

								if product.type != _type:
									product.type = _type
									change = True

								if product.url != url:
									product.url = url
									change = True

								if product.collection != collection:
									product.collection = collection
									change = True

								# Only save the Product onvce if anything has changed
								if change:
									product.save()

						# Break the parent DIV forloop, as we have found the productList
						break

			else:
				logging.error('category_url : '+category_url)
				logging.error(response.status_code)
				logging.error(response)
				raise Exception('URLFetch Error for '+category_url)
		except Exception, e:
			logging.error(self.__class__.__name__+' : Exception')
			logging.error(e)
			raise e
			

	def get(self):
		self.process()
	def post(self):
		self.process()

"""
	@name: ProductDetailCollectionKickoff
	@description:
		Long living Task for kicking off all other Product Detail collection Tasks
		This is so that the CRON job RequestHandler will not timeout, as it uses a standard webapp.RequestHandler
"""
class ProductDetailCollectionKickoff(utils.BaseHandler):
	def process(self):
		try:
			#products = models.Product.all().filter('url != ', None).filter('description = ', None).fetch(limit=None)
			products = models.Product.all().fetch(limit=None)
			
			for product in products:
				taskqueue.add(
					queue_name='productdetailcollection',
					url='/tasks/product-detail-collection',
					params={
						'product_key_name':product.key().name(),
						'product_url':product.url
					}
				)
				
			return True

		except Exception, e:
			raise e		

	def get(self):
		self.process()
	def post(self):
		self.process()

"""
	@name: ProductDetailCollection
	@description:
		Collect Product Details, including Description and Dimensions
"""
class ProductDetailCollection(utils.BaseHandler):
	def process(self):
		try:
			product_key_name = str(self.request.get('product_key_name'))
			product_url = str(self.request.get('product_url'))
			
			description = None
			width = None
			height = None
			depth = None
			length = None

			response = urlfetch.fetch(url=product_url, method=self.urlfetch['method'], deadline=self.urlfetch['deadline'], headers=self.urlfetch['headers'])

			if response.status_code == 200:

				# Get the Product
				product = models.Product.get_by_key_name(product_key_name)
				if product is not None:
					# IF we are missing a Product Description or any of the dimensions, then evaluate the HTML
					if product.description is None or product.width is None or product.height is None or product.depth is None:
						# Set the result content
						result = response.content
							
						# Parse the response content into a MiniDom object
						minidom_document = html_parser.parse_html_document(result)

						# Collect all DIV elements
						all_div_elements = minidom_document.getElementsByTagName('div')
						for div in all_div_elements:
							if 'main_product_container' in div.getAttribute('id'):
								# Get Paragraphs
								paragraphs = div.getElementsByTagName('p')
								
								for paragraph in paragraphs:
									
									if len(paragraph.childNodes) > 0:
										# Get Description
										if 'product_desc' in paragraph.getAttribute('id'):
											description = paragraph.childNodes[0].nodeValue

										# Get Dimensions
										if 'dimensions' in paragraph.getAttribute('id'):
											dim_nodes = paragraph.childNodes
											for node in dim_nodes:
												# Find the Node with Dimensions in it
												# E.g. "Bed dimensions are W7.4 x H15.8 x D7cm. More dimensions are..."
												node_name = node.nodeName
												node_value = node.nodeValue
												if node_value is not None:
													# Use the .find() method to locate the lowest index occurrence of the "cm" substring
													# Based on Habitat.co.uk Website research the convention is physical space first
													# then Usable space second
													end_of_dimensions_index = node_value.find('cm')
													if node_name == '#text':
														if end_of_dimensions_index != -1:
															dimensions_text = node_value[:end_of_dimensions_index]
															logging.debug('dimensions_text : '+dimensions_text)
															dimensions = [s.strip() for s in dimensions_text.split('x')]
															for dim in dimensions:
																if dim.find('W') != -1:
																	width = dim.replace(dim[:dim.find('W')+1],'')
																	logging.debug('width : '+str(width))
																if dim.find('H') != -1:
																	height = dim.replace(dim[:dim.find('H')+1],'')
																	if '-' in height:
																		height = height.split('-')[1]
																	logging.debug('height : '+str(height))
																if dim.find('D') != -1:
																	depth = dim.replace(dim[:dim.find('D')+1],'')
																	logging.debug('depth : '+str(depth))
																if dim.find('L') != -1:
																	length = dim.replace(dim[:dim.find('L')+1],'')
																	logging.debug('length : '+str(length))
																	
															# Break out of node loop
															break
															
								# Break out of all DIVs loop
								break

						if description is not None:
							product.description = description
						if width is not None:
							product.width = float(width)
						if height is not None:
							product.height = float(height)
						if depth is not None:
							product.depth = float(depth)
						if length is not None:
							product.length = float(length)

						product.save()

			else:
				logging.error('product_url : '+product_url)
				logging.error(response.status_code)
				logging.error(response)
				raise Exception('URLFetch Error for '+product_url)

		except Exception, e:
			logging.error(e)
			raise e
		
	def get(self):
		self.process()
	def post(self):
		self.process()