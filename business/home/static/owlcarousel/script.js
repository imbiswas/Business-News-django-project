var sectionIds = {};
$(".row-nav").each(function () {
	var $this = $(this);
	sectionIds[$this.attr("id")] = $this.first().offset().top;
});

$(window).scroll(function (event) {

	var scrolled = $(this).scrollTop();

	if (scrolled > 150) {
		$('.navbar').addClass('full-width-nav');
	} else {
		$('.navbar').removeClass('full-width-nav');
	}

	$(".row-nav").each(function () {
		var $this = $(this);

		for (key in sectionIds) {

			if (scrolled >= sectionIds[key]) {
				$(".Quick-navigation-item").removeClass("change");
				var c = $("[data-row-id=" + key + "]");
				c.addClass("change");

			}
		}
	});

});


$(".Quick-navigation-item").click(function () {

	$(this).siblings().removeClass("change");
	$(this).addClass("change");
	var i = $(this).index();
	var name = $(this).attr("data-row-id");
	var id = "#" + name;
	var top = $(id).first().offset().top - 140;

	$('html, body').animate({
		scrollTop: top + 'px'
	}, 500);

});

$("#owl-demo").owlCarousel({
	loop: true,
	margin: 30,
	autoplay: true,
	nav: true,
	dots: true,
	autoplaySpeed: 1000,
	pagination: true,
	navText: ['&#x2039', '&#x203a'],
	navContainer: ".navi",
	dotsContainer: ".dots",
	responsive: {
		0: {
			items: 1,
			nav:true
		},
		768: {
			items: 1
		},
		1170: {
			items: 1,
		}
	}
});

/*######################################
########################################    
<---------------Banner slider------------------>
########################################
######################################*/

$(".banner-slider").owlCarousel({
	items: 1,
	loop: true,
	mouseDrag: true,
	touchDrag: true,
	dots: true,
	nav: true,
	navText: ['<i class="fas fa-chevron-left"></i>', '<i class="fas fa-chevron-right"></i>'],
	autoplay: true,
	autoplayTimeout: 5000,
	autoplayHoverPause: true,
	transitionStyle: "fade",
	smartSpeed: 800,
	responsive: {
		// breakpoint from 0 up
		0: {
			nav: true,
		},
		// breakpoint from 480 up
		480: {
			nav: false,
		},
		// breakpoint from 768 up
		991: {
			nav: true,
		}
	}
});
/*######################################
########################################    
<---------------Preloader------------------>
########################################
######################################*/
$(window).on('load', function () {

	$('#preloader').addClass('loaded');
	//    preloader close
	$('.cancel-preloader').on('click', function (e) {
		e.preventDefault();
		if (!($('#preloader').hasClass('loaded'))) {
			$('#preloader').addClass('loaded');
		}
	});
});
/*######################################
########################################    
<---------------Wow JS------------------>
########################################
######################################*/
var wow = new WOW({
	boxClass: 'wow', // animated element css class (default is wow)
	animateClass: 'animated', // animation css class (default is animated)
	offset: 0, // distance to the element when triggering the animation (default is 0)
	mobile: true, // trigger animations on mobile devices (default is true)
	live: true, // act on asynchronously loaded content (default is true)
	callback: function (box) {
		// the callback is fired every time an animation is started
		// the argument that is passed in is the DOM node being animated
	},
	scrollContainer: null // optional scroll container selector, otherwise use window
});
wow.init();

/*######################################
########################################    
<---------------Navbar Icon Hamburger transition------------------>
########################################
######################################*/

$('.navbar-toggler').on('click', function () {
	$('.navbar-toggler').toggleClass('open');
});

/*######################################
########################################    
<---------------Scale out transition in footer------------------>
########################################
######################################*/

$(window).on('scroll', function () {
	if ($(window).scrollTop() + $(window).height() > $('.wrapper').outerHeight()) {
		$('.wrapper').addClass('tight');
		$('body').addClass('body-change');
	} else {
		$('.wrapper').removeClass('tight');
		// $('body').removeClass('body-change');
	}
});
$(document).load()

(function (d, s, id) {
	var js, fjs = d.getElementsByTagName(s)[0];
	if (d.getElementById(id)) return;
	js = d.createElement(s);
	js.id = id;
	js.src =
		'https://connect.facebook.net/en_US/sdk/xfbml.customerchat.js#xfbml=1&version=v2.12&autoLogAppEvents=1';
	fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));