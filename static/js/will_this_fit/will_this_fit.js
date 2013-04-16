var my_reg;
var defaultCarImg = '/static/images/cars/2061111101338.jpg';

$(document).ready(function(){

	/*
	 * Start: Will this fit in my car?
	 */
	$('.fit_in_car_btn').bind('click', function(){
		
		$('.overlay').fadeIn('fast');
		$('.panel, #car_reg_form').show();

		// Set overlay to 100% height (for IE)
		var b_height = $("body").height();
		if(b_height !== 0){
			$('.overlay').css('height', b_height+'px');
		}
	});


	/*
	 * On car reg form submit
	 */
	$('#my_reg_form').bind('submit', function() {

		// get all the inputs into an array.
		my_reg = $('#car_reg').val();

		$('.panel').attr('id', 'wide_panel');

		getCarData(my_reg);

		return false;
	});


	/*
	 * Close overlay
	 */
	$('.overlay, #close').bind('click', function(){
		
		$('.overlay, .panel, #loader, #your_car').hide();
		animatePanel("small", function(){});
	});


	/*
	 * RESET STATUS 
	 */
	$('.start_again_btn').bind('click', function(){
		
		my_reg = null;
		
		//reset car reg number and bring up panel
		$("#car_reg_form").slideDown();
		$("#your_car, #error").hide();
		
		//clear input text field
		$('#car_reg').val('');
		animatePanel("small", function(){});
	});
});


/*
 * Does this product fit in my car?
 */
function doesItFit(width, height, length){
	
	var score = [width, height, length];
		
	if(score[0] == 'yes' && score[1] == 'yes' && score[2] == 'yes'){
		
		//product fits
		yes_or_no('yes');
		
	} else if($.inArray('no', score) !== -1){
		
		//product wont fit
		yes_or_no('no');
	} else if($.inArray('maybe', score) !== -1){
		
		//product might fit
		yes_or_no('maybe');

	} else{
		console.log("nothing");
	}
}

	
/*
 * Sort JSON Car data
 */
function sortCarData(data){
	
	var make_model           = data.dvla.MAKEMODEL;
	var make                 = data.dvla.MAKE;
	var model                = data.dvla.MODEL;
	var colour               = data.dvla.COLOUR;
	var car_type             = data.dvla.DOORPLANLITERAL;
	var door_plan            = data.dvla.DOORPLAN;
	var thumb_img            = data.datastore.images.front_view;
	
	//Boot sizes
	var boot_width_top       = data.datastore.boot_aperture_width_top;
	var boot_width_middle    = data.datastore.boot_aperture_width_middle;
	var boot_width_bottom    = data.datastore.boot_aperture_width_bottom;
	
	var boot_width_sizes     = [boot_width_top, boot_width_middle, boot_width_bottom];
	var boot_width           = findLowest(boot_width_sizes);
	
	var boot_vertical_height = data.datastore.boot_aperture_verticalheight;
	var boot_aperture_height = data.datastore.boot_aperture_height;
	
	var boot_height_sizes    = [boot_vertical_height, boot_aperture_height];
	var boot_height          = findLowest(boot_height_sizes);
	
	var boot_depth           = data.datastore.boot_length;
	
	//score data
	var yom                  = data.datastore.YEAROFMANUFACTURE;
	var score_width          = data.score.width;
	var score_height         = data.score.height;
	var score_length         = data.score.length;

	doesItFit(score_width, score_height, score_length);
	displayCarData(make_model, colour, car_type, door_plan, boot_width, boot_height, boot_depth, thumb_img);

	animatePanel("large", function(){

		//Start pie animation
		calculateMatch(make, model, yom, door_plan);
	});
}


/*
 * Sort out array and find lowest number 
 */
function findLowest(arr){
	var sizes = arr;

	sizes.sort(function(a, b) { 
		return a - b;
	});

	if(sizes[0] !== null){
		return sizes[0];
	}
}


/*
 * Display car data on page
 */
function displayCarData(make_model, colour, car_type, door_plan, boot_width, boot_height, boot_depth, thumb_img){
	
	//Show product data
	displayProductData();

	var door_plan_trim = Math.round(door_plan);
	
	var car_title = make_model+' '+colour+' '+car_type+' '+door_plan_trim+' door';
	var car_title_lower = car_title.toLowerCase();

	$('#ow').html(boot_width);
	$('#oh').html(boot_height);
	$('#d').html(boot_depth);

	//Add content to container
	$('#car_name').html(car_title_lower);

	//thumbnail image
	if(thumb_img !== "" || thumb_img !== null){
		$('#car').attr('src', thumb_img).error(function() {
			//image can't be found so set back to default
			$('#car').attr('src', defaultCarImg);
		});
	}
}


/*
 * Customise panel
 */
function yes_or_no(answer){

	var list = $("#item_list");

	if(answer == 'yes'){

		$('#click_and_collect').removeClass('std_btn').addClass('orange_btn');
		$('#add_to_trolley').removeClass('orange_btn').addClass('std_btn');
		
		list.attr('class', 'yes_item_list');
		$('#yes_wrapper, #click_and_collect, #add_to_trolley').show();
		$('.result_wrapper:not("#yes_wrapper")').hide();

	}else if(answer == 'maybe'){

		$('#click_and_collect').removeClass('orange_btn').addClass('std_btn');
		$('#add_to_trolley').removeClass('std_btn').addClass('orange_btn');

		list.attr('class', 'no_item_list');
		$('#maybe_wrapper, #add_to_trolley, #click_and_collect').show();
		$('.result_wrapper:not("#maybe_wrapper")').hide();

	}else if(answer == 'no'){

		$('#click_and_collect').removeClass('orange_btn').addClass('std_btn');
		$('#add_to_trolley').removeClass('std_btn').addClass('orange_btn');
		
		list.attr('class', 'no_item_list');
		$('#no_wrapper, #add_to_trolley').show();
		$('#click_and_collect').hide();
		$('.result_wrapper:not("#no_wrapper")').hide();
	}
}


/*
 * Animate width of panel based on panel to show
 */
function animatePanel(panel, callback){

	var sidebar  = $('#sidebar_wrapper');
	var your_car = $('#your_car');
	var answer;

	if(panel == "small"){

		animatePanelWidth(551);
		sidebar.hide("slide", { direction: "left" }, 800, function(){

			answer = true;
		});

	}else if(panel == "large"){

		animatePanelWidth(772);
		your_car.slideDown('fast');
		sidebar.show("slide", { direction: "left" }, 800, function(){

			answer = true;
		});

	}else{
		answer = false;
	}

	callback(answer);
}


/*
 * Animate panel based on width provided
 */
function animatePanelWidth(p_width){

	var margin = p_width / 2;
	var margin_string = '-'+margin +'px';

	$('.panel').animate({
		width: p_width+"px",
		marginLeft: margin_string
	}, 800, function() {

		return true;
	});
}