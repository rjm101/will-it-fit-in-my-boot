#!/usr/bin/env python
from google.appengine.dist import use_library
use_library('django', '1.2')
import logging
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

#Local scripts
from controllers import default_controller
from controllers import tasks
from controllers import cron

# System URLs
requestWarmUp = '/_ah/warmup'

# JSON service URLs

# User Request Endpoint URL for HTML
requestDefault = '/'
# Homebase related pages
requestHomebase = '/homebase'
requestHomebaseProduct1 = '/homebase/product1'
requestHomebaseProduct2 = '/homebase/product2'
requestHomebaseProduct3 = '/homebase/product3'

#argos
requestArgos = '/argos'
requestArgosProduct1 = '/argos/product1'
requestArgosProduct2 = '/argos/product2'
requestArgosProduct3 = '/argos/product3'

# Task URLs
taskProductCollection = '/tasks/product-collection'
taskProductDetailCollection = '/tasks/product-detail-collection'
taskProductDetailCollctionKickoff = '/tasks/product-detail-collection-kickoff'

# CRON URLs
cronProductCollection = '/cron/product-collection'
cronProductDetailCollection = '/cron/product-detail-collection'

application = webapp.WSGIApplication([
	(requestWarmUp, default_controller.WarmupHandler),
	#homebase
	(requestHomebase, default_controller.Homebase),
	(requestHomebaseProduct1, default_controller.HomebaseProduct1),
	(requestHomebaseProduct2, default_controller.HomebaseProduct2),
	(requestHomebaseProduct3, default_controller.HomebaseProduct3),
	#argos
	(requestArgos, default_controller.Argos),
	(requestArgosProduct1, default_controller.ArgosProduct1),
	(requestArgosProduct2, default_controller.ArgosProduct2),
	(requestArgosProduct3, default_controller.ArgosProduct3),
	],debug=True)

def main():
	logging.getLogger().setLevel(logging.DEBUG)
	run_wsgi_app(application)

if __name__ == '__main__':
	main()