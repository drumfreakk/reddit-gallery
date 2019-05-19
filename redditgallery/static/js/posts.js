
function callAjax(url, data, onSuccess){
	return $.ajax({
		url: url,
		data: data,
		type: 'POST',
		success: function(response) {
			onSuccess(response);
		},
		error: function(error) {
			console.log(error);
		}
	});	
}

var nextId;

function postSuccess(response){
	console.log('postSuccess');
	document.getElementById('content').innerHTML = response;
}

function aSubSuccess(response){
	nextId = response;
	console.log('aSubSuccess');
}

function subSuccess(response){
	console.log('subsuccess');
	document.getElementById('inner').outerHTML = response + "<div id='inner'></div>";
}

function posts_init(){

	if(document.getElementById('type').value == 'single'){
		callAjax('/p/render/', {postId : document.getElementsByClassName('postId')[0].value, gfyCat : 'true'}, postSuccess);
	} else{
		sortM = document.getElementById('sort').value
		sub = document.getElementById('subr').value
		gfy = document.getElementById('gfy').value

		data = {sort : sortM, subr : sub, next : 1}

		$.when(callAjax('/r/getNext/', data, aSubSuccess)).done(function(resp){
			console.log("got next id");
			callAjax('/p/render/', {postId : nextId, gfyCat : gfy}, subSuccess);
		});

		

//		$.when(callAjax('/p/render/', {postId : nextId, gfyCat : gfy}, subSuccess)).done(function(resp){
//			console.log("got post");
//		});

//		for(var x = 0; x < ids.length; x++){
//				$.when(loadEl()).done(function(resp){
//					console.log("Finished summin");
//				});
//		}

	}
}

