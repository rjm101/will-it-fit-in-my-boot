/*
 * Get product dimensions, return in array
 */
function getProductSize(){
	
	var productSizes = [];
	productSizes["product_width"]  = items[product_id].packed_dimensions.width;
	productSizes["product_height"] = items[product_id].packed_dimensions.height;
	productSizes["product_length"] = items[product_id].packed_dimensions.length;
	
	return productSizes;
}


/*
 * Display product information
 */
function displayProductData(){
	
	itemStageClicked = true;
	
	$('#car_reg_form').hide();
	
	var p_sizes = getProductSize();

	$('#p_length').html(p_sizes["product_length"]);
	$('#p_width').html(p_sizes["product_width"]);
	$('#p_height').html(p_sizes["product_height"]);

	$('.product_title').html(items[product_id].name);
}