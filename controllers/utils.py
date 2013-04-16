import os
import logging
import datetime
import simplejson as json
import time
from ConfigParser import ConfigParser
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError   
from google.appengine.ext.db import BadValueError
from google.appengine.runtime import DeadlineExceededError
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.api import app_identity
import logging

# Import local scripts



"""
	@description:
		Base Handler Class for all webapp.RequestHandlers
"""
class BaseHandler(webapp.RequestHandler):

	context = {}
	now = None
	
	def __init__(self):

		# Set Timestamp
		self.now = datetime.datetime.now()
		self.populateContext()
		self.status_code = 200
		self.content = ''
		self.products = []
		self.categories = []
		self.departments = []
		self.navigation = None
		self.urlfetch = dict(
			method='GET',
			deadline=50,
			headers={
				'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/535.19',
				'Accept':'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5'
			}
		)

		self.product_template=dict(
			images={
				'small':'http://media.habitat.co.uk/pws/client/images/catalogue/products/@id@/small/@id@.jpg',
				'thumb':'http://media.habitat.co.uk/pws/client/images/catalogue/products/@id@/thumb/@id@.jpg',
				'medium':'http://media.habitat.co.uk/pws/client/images/catalogue/products/@id@/medium/@id@.jpg',
				'large':'http://media.habitat.co.uk/pws/client/images/catalogue/products/@id@/large/@id@.jpg'
			}
		)

	def populateContext(self):

		self.context['now'] = self.now
		self.context['request_args'] = None
		# Get the current GAE Application
		self.context['gae_application_id'] = app_identity.get_application_id()
		self.context['build_version'] = os.environ['CURRENT_VERSION_ID']
			
	def set_request_arguments(self):
		request_args = dict()
		for arg in self.request.arguments():
			request_args[str(arg)] = str(self.request.get(arg))
				
		self.context['request_args'] = request_args
		
		logging.debug(self.context['request_args'])

		return
	
	def set_response_error(self, error, status_code):
		self.context['error'] = error
		self.response.set_status(status_code)
		return

	def render(self, template_name):
		path = os.path.join(os.path.dirname(__file__),'../views/'+template_name+'.html')
		self.response.out.write(template.render(path, self.context))
		return

	def render_json(self):
		self.data_output = json.dumps(self.content)
		if self.status_code is not None:
			self.response.set_status(self.status_code)
		else:
			self.response.set_status(200)
		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(self.data_output)
		return

	def output_response(self, responseMessage, **kwargs):
		if kwargs.has_key('status_code'):
			self.response.set_status(kwargs['status_code'])			
		self.response.out.write(responseMessage)
		return


	def authenticate_admin_user(self):
		user = None
		is_system_admin= False
		try:
			user = users.get_current_user()
			
			if user is None:
				logging.error('utils.BaseHandler() : authenticate_admin_user() : user was None')
				raise Exception('Unable to get User from GAE API')
			
			is_system_admin = users.is_current_user_admin()
			self.admin_user = dict(
				user=user,
				is_system_admin=is_system_admin,
				logout_url=users.create_logout_url("/")
			)
			self.context['admin_user'] = self.admin_user

			return self.context['admin_user']
		except Exception, e:
			logging.error('utils.BaseHandler() : authenticate_admin_user()')
			logging.error(e)
			raise

def create_json_output(db_query_object):
	try:
		output = list()
		null = 'null'
		for item in db_query_object:
			job = dict()
			# Set the Job Reference Number
			job['id'] = str(item.key().name())

			# Now for each Job property...
			for key, value in item.properties().items():
				# Do not output the full Job Details summary in the JSON response for Jobs
				if key != 'details_summary':
					resource_value = getattr(item, key)
				
				if type(resource_value) == datetime.datetime:
					job[key] = resource_value.isoformat('T')				
				
				elif resource_value == None:
					job[key] = null
				# If the Property is a ReferenceProperty
				elif type(resource_value) == models.Department or type(resource_value) == models.Location or type(resource_value) == models.Division:
					job[key] = dict()
					job[key]['id'] = str(resource_value.key().name())
					for k, v in resource_value.properties().items():
						v_value = getattr(resource_value, k)
						if type(v_value) == datetime.datetime:
							job[key][k] = v_value.isoformat('T')
						elif v_value == None:
							job[key][k] = null
						else:
							job[key][k] = str(v_value)
				# Else it's an unknown property and may cause JSON dumps errors
				else:
					job[key] = str(resource_value)
			output.append(job)
		return output
	except Exception, e:
		logging.error(e)
		raise e


def load_property_file(file_name):
	try:
		property_file = memcache.get(file_name+'.properties', namespace='razorfish')
		if property_file is not None:
			return property_file
		else:
			property_file_path = 'properties/'+file_name+'.properties'
			property_file = ConfigParser()
			property_file.read(property_file_path)
			memcache.set(file_name+'.properties', property_file, namespace='razorfish')
			return property_file
	except Exception, e:
		logging.error(e)
		raise
