

function loadHoverElements(){
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
}

function hover_init(){
}
