from google.appengine.api import memcache
import os
import re
import time
import logging
import datetime
import simplejson as json
from google.appengine.ext import webapp
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.ext import blobstore
from google.appengine.api.datastore import Key
from google.appengine.api import taskqueue
from google.appengine.api import urlfetch
from google.appengine.api import mail
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from google.appengine.ext.db import BadValueError
from google.appengine.ext import db
from google.appengine.runtime import DeadlineExceededError
from operator import itemgetter
import urllib

# Import local scripts
from controllers import utils
from controllers import datastore
from models import models

class WarmupHandler(webapp.RequestHandler):
	def get(self):
		logging.debug('Warmup Request')
		pass

# Homebase
class Homebase(utils.BaseHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__),'../views/homebase/homebase.html')
		self.response.out.write(template.render(path,self.context))

class HomebaseProduct1(utils.BaseHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__),'../views/homebase/product1.html')
		self.response.out.write(template.render(path,self.context))

class HomebaseProduct2(utils.BaseHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__),'../views/homebase/product2.html')
		self.response.out.write(template.render(path,self.context))

class HomebaseProduct3(utils.BaseHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__),'../views/homebase/product3.html')
		self.response.out.write(template.render(path,self.context))

#Argos
class Argos(utils.BaseHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__),'../views/argos/argos.html')
		self.response.out.write(template.render(path,self.context))

class ArgosProduct1(utils.BaseHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__),'../views/argos/product1.html')
		self.response.out.write(template.render(path,self.context))

class ArgosProduct2(utils.BaseHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__),'../views/argos/product2.html')
		self.response.out.write(template.render(path,self.context))

class ArgosProduct3(utils.BaseHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__),'../views/argos/product3.html')
		self.response.out.write(template.render(path,self.context))
