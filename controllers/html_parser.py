import os
import logging
import datetime
import base64
import re
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
from google.appengine.runtime import DeadlineExceededError
from google.appengine.runtime import apiproxy_errors 
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from google.appengine.ext.db import BadValueError
from google.appengine.api import images
import simplejson as json
from collections import deque
from operator import itemgetter


# Import local libraries and scripts
import html5lib
from html5lib import treebuilders, treewalkers, serializer

def parse_html_document(response_body, **kwargs):
	try:

		# Create Parser
		parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("dom"))
		
		# Create MiniDom Document
		minidom_document = parser.parse(response_body)

		return minidom_document
		
		
	except Exception, e:
		logging.error('parse_category_document() : Exception')
		logging.error(e)
		raise e

