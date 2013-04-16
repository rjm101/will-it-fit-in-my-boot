//Product sidebar template
var sidebarListItem = '<li><a href="javascript:void(0);"><img src="@path@@product_img@" alt="@product_title@" class="product_thumb" data-id="@key_id@"></a><a href="javascript:void(0);" class="product_title" data-id="@key_id@">@product_title@</a></li>';

$(document).ready(function(){

	/*
	 * Loop through product array and propulate sidebar
	 */
	$.each(items, function(key, value){

		var id = key;
		var product_title = items[key].name;
		var product_img = items[key].thumb_img;

		var tag_list = ['@path@', '@product_img@', '@product_title@', '@key_id@'];
		var var_references = [product_url, product_img, product_title, id];

		replaceKeyData(tag_list, var_references, sidebarListItem, $('#product_selection'));
	});

});


/* Template HTML symbol replacer -- @something@ 
 * items {array} contains strings '@word@'
 * varReferences {array} contains data to be added
 * Note: items and varReferences array must be in same order! 
*/
function replaceKeyData(items, varReferences, templateHTML, container){
	
	if(items.length == varReferences.length && templateHTML !== null && container !== null){
		
		for(var i = 0; i < items.length; i++){
			
	
			//.replace only works once so count how many words matching '@word@' are contained within string
			var num_of_matching_words = occurrences(templateHTML, items[i], false);
			
			for(var j = 0; j < num_of_matching_words; j++){
			
				templateHTML = templateHTML.replace(items[i]+"", varReferences[i]);
			}
		
			
			//end		
			var end_point = items.length -1;

			if(i == end_point){

				container.append(templateHTML);
								
				return true;
			}
		}
		
	}else{	
		
		//error messages
		if(items.length !== varReferences.length){
			//console.log("Variable array and reference replace array are not the same length!");
		}
		
		if(container == null){
			//console.log("Container doesnt exist");
		}
		
		if(templateHTML == null || templateHTML == ''){
			//console.log("HTML is empty");
		}
	}
}


/* Function count the occurrences of substring in a string;
 * @param {String} string   Required. The string;
 * @param {String} subString    Required. The string to search for;
 * @param {Boolean} allowOverlapping    Optional. Default: false;
 */
function occurrences(string, subString, allowOverlapping){

    string+="";
    subString+="";

    if(subString.length<=0) return string.length+1;

    var n=0, pos=0;
    var step=(allowOverlapping)?(1):(subString.length);

    while(true){
		pos=string.indexOf(subString,pos);
		if(pos>=0){ n++; pos+=step; } else break;
    }
    return(n);
}
