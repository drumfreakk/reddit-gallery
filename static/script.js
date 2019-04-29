
function vote(type, postId){
$.ajax({
            url: '/vote/vote',
            data: {id: postId, voteType: type},
            type: 'POST',
            success: function(response) {
				if (type == 'up'){
					document.getElementById(postId.concat('down')).className = 'notDown';
					if (document.getElementById(postId.concat(type)).className == 'notUp'){
						document.getElementById(postId.concat(type)).className = 'up';
					} else if (document.getElementById(postId.concat(type)).className == 'up'){
						document.getElementById(postId.concat(type)).className = 'notUp';
					}
				} else if (type == 'down'){
					document.getElementById(postId.concat('up')).className = 'notUp';
					if (document.getElementById(postId.concat(type)).className == 'notDown'){
						document.getElementById(postId.concat(type)).className = 'down';
					} else if (document.getElementById(postId.concat(type)).className == 'down'){
						document.getElementById(postId.concat(type)).className = 'notDown';
					}
				} else {
					document.getElementById(postId.concat('up')).className = 'notUp';
					document.getElementById(postId.concat('down')).className = 'notDown';
				}
                
            },
            error: function(error) {
                console.log(error);
            }
        });
}

function save(postId){
$.ajax({
            url: '/save/save',
            data: {id: postId},
            type: 'POST',
            success: function(response) {
				console.log('wot');
				if (document.getElementById(postId.concat('save')).innerHTML == 'Save'){
					document.getElementById(postId.concat('save')).className = 'save';
					document.getElementById(postId.concat('save')).innerHTML = 'Unsave';
				} else if (document.getElementById(postId.concat('save')).innerHTML == 'Unsave'){
					document.getElementById(postId.concat('save')).className = 'notSave';
					document.getElementById(postId.concat('save')).innerHTML = 'Save';
				}
            },
            error: function(error) {
                console.log(error);
            }
        });
}
