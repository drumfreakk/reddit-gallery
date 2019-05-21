

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


var myopacity = 0;

function fadeIn() {
   if (myopacity<1) {
      myopacity += .075;
     setTimeout(function(){MyFadeFunction()},100);
   }
   document.getElementById('navbar').style.opacity = myopacity;
}

function fadeOut() {
   if (myopacity>0) {
      myopacity -= .075;
     setTimeout(function(){MyFadeFunction()},100);
   }
   document.getElementById('navbar').style.opacity = myopacity;
}


var lastScrollTop = 0;
$(window).scroll(function(event){
   var st = $(this).scrollTop();
   if (st > lastScrollTop){
       fadeOut();
   } else {
      fadeIn();
   }
   lastScrollTop = st;
});

window.onscroll = function(ev) {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
		window.scrollBy(0, -100);
		loadEls();
    }
};

