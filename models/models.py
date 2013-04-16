from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
import logging
import datetime
import time

SIMPLE_TYPES = (int, long, float, bool, dict, basestring)

class BaseModel(db.Model):
	created = db.DateTimeProperty(
	    auto_now_add=True,
	    indexed=True
	)
	last_modified = db.DateTimeProperty(
	    auto_now=True,
	    indexed=True
	)
	def save(self):
		try:
			def txn():
				return self.put()
			return db.run_in_transaction(txn)
		except CapabilityDisabledError, capability_error:
			logging.error(self.__class__.__name__+' : CapabilityDisabledError')
			logging.error(capability_error)
			raise
		except Exception, e:
			logging.error(self.__class__.__name__+' : Exception')
			logging.error(e)
			raise
	def to_dict(self):
		#return dict([(p, unicode(getattr(self, p))) for p in self.properties()])
		output = {}
		for key, prop in self.properties().iteritems():
			value = getattr(self, key)
			if value is None or isinstance(value, SIMPLE_TYPES):
				# Do not include None as a value
				output[key] = value or ''
			elif isinstance(value, datetime.datetime) or isinstance(value, datetime.date):
				# Convert date/datetime to ms-since-epoch ("new Date()").
				ms = time.mktime(value.utctimetuple())
				ms += getattr(value, 'microseconds', 0) / 1000
				output[key] = int(ms)
			elif isinstance(value, Category):
				output[key] = value.name
				# Additionally add the Department just as a product dict property
				output['department'] = value.department.name
			elif isinstance(value, Department):
				output[key] = value.name
			elif isinstance(value, list):
				output[key] = [db.get(i).to_dict() for i in value]
			else:
				raise ValueError('cannot encode ' + repr(prop))
			# Add Key NAme or ID
			output['key'] = self.key().name() or self.key().id()
		
		return output

class Department(BaseModel):
	name = db.StringProperty(
		indexed=True,
		required=False
	)

class Category(BaseModel):
	name = db.StringProperty(
		indexed=True,
		required=False
	)
	department = db.ReferenceProperty(
		Department,
		collection_name='categories',
		indexed=True,
		required=False
	)

class Image(BaseModel):
	type = db.StringProperty(
		choices=set(['small','thumb','medium','large'])
	)
	url = db.LinkProperty(
		required=True,
		indexed=False
	)

class Product(BaseModel):
	name = db.StringProperty(
		indexed=True,
		required=False
	)
	category = db.ReferenceProperty(
		Category,
		collection_name='products',
		indexed=True,
		required=False
	)
	# Keep a String reference to the Department key_name
	department = db.StringProperty(
		indexed=True,
		required=False
	)
	collection = db.StringProperty(
		required=False,
		indexed=True
	)
	type = db.CategoryProperty(
		indexed=True,
		required=False
	)
	price = db.FloatProperty(
		indexed=True,
		required=False
	)
	# Some Products may not have a width and instead just a Depth, eg. for Diameter
	width = db.FloatProperty(
		indexed=True,
		required=False
	)
	height = db.FloatProperty(
		indexed=True,
		required=False
	)
	depth = db.FloatProperty(
		indexed=True,
		required=False
	)
	# Some products may have just a length
	length = db.FloatProperty(
		indexed=True,
		required=False
	)
	colour = db.StringProperty(
		indexed=True,
		required=False,
		choices=set([
			'black',
			'blue',
			'bronze',
			'brown',
			'clear',
			'gold',
			'green',
			'grey',
			'metallics',
			'mirrored',
			'multi-coloured',
			'natural',
			'neutral',
			'orange',
			'pink',
			'purple',
			'red',
			'silver',
			'white',
			'yellow',
			''
		])
	)
	description = db.TextProperty(
		required=False
	)
	images = db.ListProperty(
		db.Key,
		required=True,
		indexed=False
	)
	url = db.LinkProperty(
		required=False,
		indexed=True
	)

departments=dict(
	furniture=dict(
		beds='http://www.habitat.co.uk/beds/furniture/fcp-category/list?productsPerPage=200',
		drawers='http://www.habitat.co.uk/bedside-drawers/furniture/fcp-category/list?productsPerPage=200',
		chairsandbenches='http://www.habitat.co.uk/chairs-benches/furniture/fcp-category/list?productsPerPage=200',
		coffeetables='http://www.habitat.co.uk/coffee-table/furniture/fcp-category/list?productsPerPage=200',
		desks='http://www.habitat.co.uk/desks-worktops/furniture/fcp-category/list?productsPerPage=200',
		diningtables='http://www.habitat.co.uk/dining-tables/furniture/fcp-category/list?productsPerPage=200',
		mattresses='http://www.habitat.co.uk/mattresses/furniture/fcp-category/list?productsPerPage=200',
		mirrors='http://www.habitat.co.uk/mirrors/furniture/fcp-category/list?productsPerPage=200',
		rugs='http://www.habitat.co.uk/rugs-floor-coverings/furniture/fcp-category/list?productsPerPage=200',
		sidetables='http://www.habitat.co.uk/side-tables/furniture/fcp-category/list?productsPerPage=200',
		storageandshelving='http://www.habitat.co.uk/shelves-storage/furniture/fcp-category/list?productsPerPage=200',
		tablesandconsoles='http://www.habitat.co.uk/tables-consoles/furniture/fcp-category/list?productsPerPage=200',
		wardrobes='http://www.habitat.co.uk/wardrobes/furniture/fcp-category/list?productsPerPage=200'
	),
	lighting=dict(
		bulbs='http://www.habitat.co.uk/bulbs/lighting/fcp-category/list?productsPerPage=200',
		decorativelights='http://www.habitat.co.uk/decorative-lights-garlands/lighting/fcp-category/list?productsPerPage=200',
		floorlamps='http://www.habitat.co.uk/floor-lights/lighting/fcp-category/list?productsPerPage=200',
		lampshades='http://www.habitat.co.uk/light-shades/lighting/fcp-category/list?productsPerPage=200',
		pendants='http://www.habitat.co.uk/pendants-accessories/lighting/fcp-category/list?productsPerPage=200',
		spotlights='http://www.habitat.co.uk/spot-lights/lighting/fcp-category/list?productsPerPage=200',
		tablelamps='http://www.habitat.co.uk/table-lights/lighting/fcp-category/list?productsPerPage=200'
	),
	sofas=dict(
		webexclusives='http://www.habitat.co.uk/exclusive/sofas/fcp-category/list?productsPerPage=200',
		twoseat='http://www.habitat.co.uk/2seat/sofas/fcp-category/list?productsPerPage=200',
		threeseat='http://www.habitat.co.uk/3seat/sofas/fcp-category/list?productsPerPage=200',
		fourseat='http://www.habitat.co.uk/4seat/sofas/fcp-category/list?productsPerPage=200',
		armchairsfootstools='http://www.habitat.co.uk/armchairs-footstools/sofas/fcp-category/list?productsPerPage=200',
		chaise='http://www.habitat.co.uk/chaise/sofas/fcp-category/list?productsPerPage=200',
		compact='http://www.habitat.co.uk/compact/sofas/fcp-category/list?productsPerPage=200',
		fabric='http://www.habitat.co.uk/fabric/sofas/fcp-category/list?productsPerPage=200',
		leather='http://www.habitat.co.uk/leather/sofas/fcp-category/list?productsPerPage=200',
		modular='http://www.habitat.co.uk/modular/sofa/fcp-category/list?productsPerPage=200',
		sofabeds='http://www.habitat.co.uk/sofabeds/sofas/fcp-category/list?productsPerPage=200'
	)
)
