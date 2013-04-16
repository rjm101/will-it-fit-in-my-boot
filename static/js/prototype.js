//Global vars
var product_id;

$(document).ready(function(){
	
	/* 
	 * Listen for product click
	 */
	$(document).on("click", '.product_thumb, .product_title', function(){
		
		var _this = $(this);
		newItemClick(_this);
	});
	
	
	/*
	 * Trigger new item
	 */
	function newItemClick(_this){
		
		var clicked_item_id = _this.attr('data-id');

		if(typeof items[clicked_item_id] === 'undefined'){
			
			//alert("product not found");
		}else{
			
			resetState();
			loadProduct(clicked_item_id);
		}
	}
	
	
	/*
	 * Reset Overlay States
	 */
	function resetState(){
		my_reg           = null;
		product_id       = null;

		$('#slide_arrow').css('height', '302px');
		$('#product_selection').slideDown();
		$('.overlay, #your_car, #content_area').hide();
	}


	/*
	 * Start: Will this fit in my car?
	 */
	$('.fit_in_car_btn').bind('click', function(){
		
		$("#product_menu_box").toggleClass('slide_menu_box').animate({
			top: '90px'
		}, 1000);
		$('#car_regs').slideDown();
		
		//HIDE PRODUCTS
		$('#product_selection').slideUp();
		$('#slide_arrow').css('height', '219px');
	
		//store product_id
		product_id = $(this).attr('data-id');

		$('#panel_product').attr('src', product_url+items[product_id].thumb_img);
	});
	
		
	/*
	 * Close overlay
	 */
	$('.overlay, #close').bind('click', function(){
		
		$('#product_selection').slideDown();
		$("#product_menu_box").animate({
			top: '210px'
		}, 1000);
		$('#car_regs').slideUp();
		$('#slide_arrow').css('height', '302px');
	});
	
	
	/* 
	 * Hide/show user scenario panel 
	 */
	$('#slide_arrow').bind('click', function(){
	
		$("#product_menu_box").toggleClass('slide_menu_box');
	});
	
	
	/* 
	 * Add car reg to input field 
	 */
	$('#reg_nos li a').bind('click', function(){
		
		$('#car_reg').val($(this).attr('data-id'));
	});
});