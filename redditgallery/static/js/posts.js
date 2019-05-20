
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

function empty(){}

function postSuccess(response){
	document.getElementById('content').innerHTML = response;
	loadHoverElements();
}


function getIds(next){
	return callAjax('/r/getNext/', {sort : sortM, subr : sub, next : next}, empty);
}

function getPost(id){
	return callAjax('/p/render/', {postId : id, gfyCat : gfy}, empty);
}

function loadFiveEls(){
	if(allowLoad == false){
		return;
	}

	var max_tmp = max;
	var doing_tmp = doing;

	var reset = false;

	if(working == true){
		doing = 'inner';
		reset = true;
	} else {
		doing = 'inner_2';
	}

	working = true;
	$.when(getIds(max_tmp), getIds(max_tmp + 1), getIds(max_tmp + 2), getIds(max_tmp + 3), getIds(max_tmp + 4)).done(function(first, second, third, fourth, fifth){
		$.when(getPost(first[0]), getPost(second[0]), getPost(third[0]), getPost(fourth[0]), getPost(fifth[0])).done(function(firstB, secondB, thirdB, fourthB, fifthB){
			document.getElementById(doing_tmp).outerHTML = firstB[0] + secondB[0] + thirdB[0] + fourthB[0] + fifthB[0] + "<div id='" + doing_tmp + "'></div>";
			working = false;
			loadHoverElements();
			if(reset == true){
				allowLoad = true;
			}
		});
	});
	max = max_tmp + 5;
}

function loadEls(){
	loadFiveEls();
	loadFiveEls();
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

window.onscroll = function(ev) {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
		window.scrollBy(0, -100);
		loadEls();
    }
};

