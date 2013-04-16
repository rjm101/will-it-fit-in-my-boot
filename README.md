# CRON Jobs

Load this URL in a web browser to kick off Product and Product Detail collection Jobs.

WARNING: There are many thousands of Products to collect. These Product collection jobs run as Tasks on your local machine at a deliberately slow rate. This may make your local web application unresponsive whilst the Product collection jobs are running, so only run these jobs periodically and allow 30 minutes or so for full data collection.

## Product Collection

Takes approx. 2-3 minutes

* /cron/product-collection

## Product Detail Collection

Takes approx. 30 minutes

* /cron/product-detail-collection



# JSON Services

Live Development site:

* http://phoenix-habitat.appspot.com


## Navigation

You can query the full set of Departments and their Categories at the following URL

* /json/navigation

This will return a Navigation object in the following data format:

{
	"Furniture":[
		"Beds",
		"Chairs"
	],
	"Lighting":[
		"Lamps",
		"Bulbs"
	]
}


## Departments

You can query Departments at the following URL

* /json/departments

This will return Departments in the following data format:

{
	"response":"Departments",
	"data":[
		{
			"key":"furniture",
			"name":"Furniture"
		},
		{
			"key":"lighting",
			"name":"Lighting"
		},
		... next category
	]
}

## Categories

You can query Categories at the following URL

* /json/categories

This will return Categories in the following data format:

{
	"response":"Categories",
	"data":[
		{
			"key":"beds",
			"name":"Beds"
		},
		{
			"key":"wardrobes",
			"name":"Wardrobes"
		},
		... next category
	]
}


## Products

You can query Products at the following URL

* /json/products

This will return Products in the following data format:

{
	"response":"Products",
	"data":[
		{
			"key":"12345",
			"name":"Iona King Size Bed"
			"category":"Beds",
			"department":"Furniture",
			"description":"",
			"price":500.50,
			"created":134567867,
			"last_modified":134567867,
			"type":"kingsize",
			"colour":"red",
			"images":[
				{
					"url": "http://media.habitat.co.uk/pws/client/images/catalogue/products/12345/medium/12345.jpg",
					"last_modified": 1362338042, 
					"type": "medium", 
					"key": 75303, 
					"created": 1362338042
				},
				... next Image
			]
			"url":"http://"
		},
		... next Product
	]
}

NOTE: You can combine any of the filters below when querying Products. It doesn't matter which order the filter is applied as a URL query parameter, e.g. /?foo=1&bar=2 is the same as /?bar=2&foo=1.

### Filter: All Products

This will give you all Products - careful there may be thousands!

* /json/products

NOTE: the default limit of products you will receive back is 25. This will be the first 25 that the Datastore returns without any additional filters, so it could be anything.

### Filter: Products with a defined limit

* /json/products?limit=N

Where N is any number for the quantity of products to get.

Examples:

* /json/products?limit=4 (get the first 4 Products)
* /json/products?limit=100 (get the first 100 Products)
* /json/products?limit=10000 (may take some time)

### Filter: Products by Category

* /json/products?category=CATEGORY_KEY

Where CATEGORY_KEY is a valid Category Key (ID). 

See the JSON service for Categories above for how to get a list of available Categories and their keys.

The general rule is that the Category Key is the Category display name, with whitespace removed and in lower case. E.g. A Category with a display name of "This and That" would have a Key of "thisandthat".

Examples:

* /json/products?category=beds (just get Bed Products)
* /json/products?category=wardrobes (just get Wardrobe Products)


### Filter: Products by Collection

* /json/products?collection=COLLECTION_NAME

Where COLLECTION_NAME is an available Collection (client-defined brand taxonomy) for a Product

Examples:

* /json/products?collection=iona
* /json/products?collection=gisele
* /json/products?collection=rosso

### Filter: Products by Price Min, Price Max or Price Range

* /json/products?priceMin=N
* /json/products?priceMax=N
* /json/products?priceMin=N1&priceMax=N2

Where N is a price value, and N1 is the lowest price and N2 is the highest price.

Examples:

* /json/products?priceMin=500 (all Products greater than or equal to £500)
* /json/products?priceMax=500 (all Products less than or equal to £500)
* /json/products?priceMin=250&priceMax=500 (all Products between £250 and £500)

### Filter: Products by Colour

* /json/products?colour=COLOUR

Where COLOUR is an available colour

Examples:

* /json/products?colour=black
* /json/products?colour=blue
* /json/products?colour=natural

Available colours:

* black
* blue
* bronze
* brown
* clear
* gold
* green
* grey
* metallics
* mirrored
* multi-coloured
* natural
* neutral
* orange
* pink
* purple
* red
* silver
* white
* yellow

### All Product Filters

Here's an example of all filters in a single request:

* /json/products?category=beds&priceMin=250&priceMax=500&limit=10

This would return Beds only, with a price of between £250-£500 only, and up to 10 of them.