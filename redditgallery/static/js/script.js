
function vote(type, postId){
$.ajax({
            url: '/p/'.concat(postId).concat('/vote'),
            data: {voteType: type},
            type: 'POST',
            success: function(response) {
				if (type == 'up'){
					document.getElementById(postId.concat('down')).className = 'notDown downv';
					if (document.getElementById(postId.concat(type)).className == 'notUp upv'){
						document.getElementById(postId.concat(type)).className = 'up upv';
					} else if (document.getElementById(postId.concat(type)).className == 'up upv'){
						document.getElementById(postId.concat(type)).className = 'notUp upv';
					}
				} else if (type == 'down'){
					document.getElementById(postId.concat('up')).className = 'notUp upv';
					if (document.getElementById(postId.concat(type)).className == 'notDown downv'){
						document.getElementById(postId.concat(type)).className = 'down downv';
					} else if (document.getElementById(postId.concat(type)).className == 'down downv'){
						document.getElementById(postId.concat(type)).className = 'notDown downv';
					}
				} else {
					document.getElementById(postId.concat('up')).className = 'notUp upv';
					document.getElementById(postId.concat('down')).className = 'notDown downv';
				}
                
            },
            error: function(error) {
                console.log(error);
            }
        });
}

function save(postId){
$.ajax({
            url: '/p/'.concat(postId).concat('/save'),
            data: {},
            type: 'POST',
            success: function(response) {
				if (document.getElementById(postId.concat('save')).innerHTML == 'Save'){
					document.getElementById(postId.concat('save')).className = 'save savev';
					document.getElementById(postId.concat('save')).innerHTML = 'Unsave';
				} else if (document.getElementById(postId.concat('save')).innerHTML == 'Unsave'){
					document.getElementById(postId.concat('save')).className = 'notsave savev';
					document.getElementById(postId.concat('save')).innerHTML = 'Save';
				}
            },
            error: function(error) {
                console.log(error);
            }
        });
}

$(document).ready(function(){
	$("center").hover(function(){
			var els = this.getElementsByClassName("tag");
			for(var i = 0; i < els.length; ++i){
				$(els[i]).css("opacity", "0.8");
			}
		}, function(){
		    var els = this.getElementsByClassName("tag");
			for(var i = 0; i < els.length; ++i){
				$(els[i]).css("opacity", "0");
			}
	 });
});



