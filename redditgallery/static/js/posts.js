
var sortM;
var sub;
var gfy;

var doing = 'inner';
var working = false;
var max = 1;

var allowLoad = true;

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

function empty(response){
}

function postSuccess(response){
	document.getElementById('content').innerHTML = response;
	loadHoverElements();
}


function getIds(next){
	return callAjax('/r/getNext/', {sort : sortM, subr : sub, next : next, render : 1, gfycat : gfy}, empty);
}

function getPost(id){
	return callAjax('/p/render/', {postId : id, gfyCat : gfy}, empty);
}


function loadEls(){
	if(allowLoad == false){
		return;
	}

	$.when(getIds(max), getIds(max + 1), getIds(max + 2), getIds(max + 3), getIds(max + 4), getIds(max + 5), getIds(max + 6), getIds(max + 7), getIds(max + 8), getIds(max + 9)).done(function(A, B, C, D, E, F, G, H, I, J){
		document.getElementById('inner').outerHTML = A[0] + B[0] + C[0] + D[0] + E[0] + F[0] + G[0] + H[0] + I[0] + J[0] + "<div id='inner'></div>";
		loadHoverElements();
		allowLoad = true;
	});
	max += 10;


	allowLoad = false;
}

function posts_init(){
	if(document.getElementById('type').value == 'single'){
		callAjax('/p/render/', {postId : document.getElementsByClassName('postId')[0].value, gfyCat : 'true'}, postSuccess);
	} else{
		sortM = document.getElementById('sort').value;
		sub = document.getElementById('subr').value;
		gfy = document.getElementById('gfy').value;

		loadEls();
	}
}

