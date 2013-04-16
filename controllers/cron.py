import os
import logging
import datetime
import base64
import cgi
import time
import urllib
import cStringIO
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.ext import blobstore
from google.appengine.api import taskqueue
from google.appengine.api import mail
from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.runtime import DeadlineExceededError
from google.appengine.runtime import apiproxy_errors 
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from google.appengine.ext.db import BadValueError
from google.appengine.api import images
import simplejson as json
from collections import deque
from operator import itemgetter

# Import local modules or scripts
from models import models
from controllers import datastore

class ProductCollection(webapp.RequestHandler):
	def process(self):
		try:
			# Check for App Engine CRON Header or System Admin access
			if not self.request.headers.has_key('X-Appengine-Cron'):
				
				# Else check for System Admin access
				is_system_admin = users.is_current_user_admin()
				
				if not is_system_admin:
					logging.warning('WARNING: Illegal access to CRON job by user')
					user = users.get_current_user()
					if user is not None:
						logging.warning('User nickname : '+str(user.nickname()))
						logging.warning('User email : '+str(user.email()))
						logging.warning('User ID : '+str(user.user_id()))
					# Return immediately and do not run the tasks
					return False
			
			# Flush the cache
			memcache.flush_all()

			for department_key, department_dict in models.departments.items():
				for category_key, category_url in department_dict.items():
					taskqueue.add(
						queue_name='productcollection',
						url='/tasks/product-collection',
						params={
							'department_key':department_key,
							'category_url':category_url
						}
					)

			return True

		except Exception, e:
			raise e		

	def get(self):
		self.process()
	def post(self):
		self.process()


class ProductDetailCollection(webapp.RequestHandler):
	def process(self):
		try:
			# Check for App Engine CRON Header or System Admin access
			if not self.request.headers.has_key('X-Appengine-Cron'):
				
				# Else check for System Admin access
				is_system_admin = users.is_current_user_admin()
				
				if not is_system_admin:
					logging.warning('WARNING: Illegal access to CRON job by user')
					user = users.get_current_user()
					if user is not None:
						logging.warning('User nickname : '+str(user.nickname()))
						logging.warning('User email : '+str(user.email()))
						logging.warning('User ID : '+str(user.user_id()))
					# Return immediately and do not run the tasks
					return False
			
			taskqueue.add(
				queue_name='productdetailcollection',
				url='/tasks/product-detail-collection-kickoff'
			)
			
			return True

		except Exception, e:
			raise e		

	def get(self):
		self.process()
	def post(self):
		self.process()