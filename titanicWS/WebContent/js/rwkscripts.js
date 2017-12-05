$(document).ready(function(){
	
	$('#RWKForm').submit( function(e) {
	    
		$('#RWKLoader').show();
		
		e.preventDefault();
		var p = [];
		
		$("#RWKForm input").each(function(){
		    p.push(this.value);
		});
		
		var params = "?Pclass="+p[0]+"&Sex="+p[1]+"&SibSp="+p[2]+"&Parch="+p[3];
		
		$.ajax({
	        url: 'http://localhost:8180/titanicWS/rest/prediction'+params,
	        type: 'GET',
	        success: function(data) {

	        	$('#RWKSubmit').hide();
	        	
	        	if(data == "You did not survive!"){
	        		$('#RWKAlert').addClass("alert-danger");
	        	}
	        	
	        	$('#RWKAlert').show();
	        	$('#RWKAlert').html(data);
	        }
	    });
		
	});
	
});
