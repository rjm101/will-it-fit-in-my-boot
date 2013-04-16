/*
 * Item details here
 */
var items = [];
items[0] = {
	
	key: '53343',
	name: 'Provence Double Wardrobe',
	packed_dimensions: {
		width: 115,
		length: 57,
		height: 130
	},
	price: 399,
	thumb_img: '790393_R_Z001.jpg'
};

items[1] = {
	
	key: '21344',
	name: 'Chester Compact Sofa - Dark Stained Feet - Beige - Fabric',
	packed_dimensions: {
		width: 70,
		length: 66,
		height: 65
	},
	price: 640,
	thumb_img: '025497_R_Z001.jpg'
};

items[2] = {
	
	key: '33421',
	name: 'Wiltshire Lamp Table Oak',
	packed_dimensions: {
		width: 55,
		length: 48,
		height: 48
	},
	price: 99.99,
	thumb_img: 'lamp_table.jpg'
};


/*
 * Load product on page load and click
 */
function loadProduct(productID){

	var product_id = productID;
	var price      = '£'+items[productID].price;
	var title      = items[productID].name;
	var thumb_img  = product_url+items[productID].thumb_img;

	//Add content to container
	$('.p_title').html(title);
	$('.price').html(price);
	$('.price_col').html(price);
	$('.product_item, .product').attr('src', thumb_img);
	$('.fit_in_car_btn, #new_reg').attr('data-id', product_id);
	
	
	$('#content_area').show();
	
	$("#product_menu_box").toggleClass('slide_menu_box');
}