/*
 * Item details here
 */
var items = [];
items[0] = {
	
	key: 'product1',
	name: 'Chad Valley 3ft 4 in 1 Multi Games Table',
	packed_dimensions: {
		width: 95.6,
		length: 23.2,
		height: 63.2
	},
	price: 69.99,
	thumb_img: 'pool.jpg',
	top_image: 'product1-top.png',
	bottom_image: 'product1-bottom.png'
};

items[1] = {
	
	key: 'product2',
	name: 'Toshiba 40BL702 40 Inch Full HD Freeview Edge-lit LED TV',
	packed_dimensions: {
		width: 74,
		length: 23.2,
		height: 63.2
	},
	price: 399,
	thumb_img: '5299036_R_Z001.jpg',
	top_image: 'product2-top.png',
	bottom_image: 'product2-bottom.png'
};

items[2] = {
	
	key: 'product3',
	name: 'Wiltshire Lamp Table Oak',
	packed_dimensions: {
		width: 41,
		length: 25,
		height: 60
	},
	price: 99.99,
	thumb_img: '4111081_R_Z001A_UC1288103.jpg',
	top_image: 'product3-top.png',
	bottom_image: 'product3-bottom.png'
};


/*
 * Load product on page load and click
 */
function loadProduct(productID){

	var product_id        = productID;
	var price             = '£'+items[productID].price;
	var title             = items[productID].name;
	var thumb_img         = product_url+items[productID].thumb_img;
	var top_page_image    = items[productID].top_image;
	var bottom_page_image = items[productID].bottom_image;
	var product           = items[productID].key;

	//clear container classes
	$('#page_container_top, #page_container_bottom').attr('class', '');

	//Add page images
	$('#page_container_top').addClass(items[productID].key+'_top');
	$('#page_container_bottom').addClass(items[productID].key+'_bottom');

	$('#reserve_container').show();

	//Add content to modal container
	$('.product').attr('src', thumb_img);

	//Fill btn with data id
	$('.fit_in_car_btn, #new_reg').attr('data-id', product_id);
	
	$("#product_menu_box").toggleClass('slide_menu_box');
}