/* Generic request JSON handler
 * Path {string} is http json path
 */
function requestHandler(path, callback){

	$.getJSON(path+'&?callback=?', null, function(data){
		
		//check if data returned contains properties within object
		//event complete so return data to caller
		callback(data);	
	})
	.success(function (){
		return true;	
	})
	 .error(function(jqXHR, textStatus, errorThrown){
        console.log(textStatus);
        console.log(jqXHR.responseText);
    });
}


/*
 * Check if data set is empty
 */
function getCarData(vrm){
	
	//validate VRM
	//var vrm_num = vrm.match(/^([A-Z]{3}\s?(\d{3}|\d{2}|d{1})\s?[A-Z])|([A-Z]\s?(\d{3}|\d{2}|\d{1})\s?[A-Z]{3})|(([A-HK-PRSVWY][A-HJ-PR-Y])\s?([0][2-9]|[1-9][0-9])\s?[A-HJ-PR-Z]{3})$/);

	//valid number plate so move on
	//if(vrm_num){
		
		$('#car_reg_form').hide();
		$('#loader').show();
		
		//Convert to uppercase and remove white space
		vrm = vrm.toUpperCase().replace(/\s+/g, '');
		
		var path = constructPath(vrm);
		
		if(path){
		
			requestHandler(path, function(data){
					
				$('#loader').fadeOut('slow', function(){
			
					if(typeof data.error !== 'undefined'){
						showError(data.error);

					}else {
						if(typeof(data.data.dvla.error) !== "undefined"){
							var error = data.data.dvla.error;
							var message = data.data.dvla.error.toLowerCase();
							showError(message);

						} else if(data.data.datastore == "float() argument must be a string or a number"){
							showError("No boot size data available");
						} else if(jQuery.type(data.data.datastore) === "object"){
							
							sortCarData(data.data);
						} else{
							showError("Sorry this car does not match our records");
						}
					}
				});
			
			});
		}
	/*}else{
		//invalid number plate
		showError("Invalid number plate");
	}*/
}


/*
 * Construction path request
 */
function constructPath(vrm){
		
	var p_sizes = getProductSize();
	var dimensions = '&width='+p_sizes["product_width"]+'&height='+p_sizes["product_height"]+'&length='+p_sizes["product_length"];

	var path = 'https://experian-services.appspot.com/?vrm='+vrm+dimensions;
	
	return path;
}


/*
 *	Display error message
 */
function showError(message){
	$('#error').show().delay(8000).fadeOut('slow');
	$('#error_message').html(message);
	$('#car_reg_form').slideDown();
}