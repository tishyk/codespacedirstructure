/**
 * @name		jQuery Countdown Plugin
 * @author		Martin Angelov
 * @version 	1.0
 * @url			http://tutorialzine.com/2011/12/countdown-jquery/
 * @license		MIT License
 */

(function($){
	
	// Number of seconds in every time division
	var days	= 24*60*60,
		hours	= 60*60,
		minutes	= 60;
	
	// Creating the plugin
	$.fn.countdown = function(prop){
		
		var options = $.extend({
			callback	: function(){},
			timestamp	: 0
		},prop);
		
		var left, d, h, m, s, positions;

		// Initialize the plugin
		init(this, options);
		
		positions = this.find('.position');
		
		(function tick(){
			
			// Time left
			left = Math.floor((options.timestamp - (new Date())) / 1000);
			
			if(left < 0){
				left = 0;
			}
			var posEx = 0;
			// Number of days left
			d = Math.floor(left / days);

			if( d >= 100 ) {
				posEx = 1;
				updateTri(0, 1, 2, d);
			} else {
				updateDuo(0+posEx, 1+posEx, d);
			}
			left -= d*days;
			
			// Number of hours left
			h = Math.floor(left / hours);
			updateDuo(2+posEx, 3+posEx, h);
			left -= h*hours;
			
			// Number of minutes left
			m = Math.floor(left / minutes);
			updateDuo(4+posEx, 5+posEx, m);
			left -= m*minutes;
			
			// Number of seconds left
			s = left;
			updateDuo(6+posEx, 7+posEx, s);
			
			// Calling an optional user supplied callback
			options.callback(d, h, m, s);
			
			// Scheduling another call of this function in 1s
			setTimeout(tick, 1000);
		})();
		
		// This function updates two digit positions at once
		function updateDuo(minor,major,value){
			switchDigit(positions.eq(minor),Math.floor(value/10)%10);
			switchDigit(positions.eq(major),value%10);
		}

		// This function updates three digit positions at once
		function updateTri(first, second, third, value){
			switchDigit(positions.eq(first),Math.floor(value/100)%100);
			switchDigit(positions.eq(second),Math.floor(value/10)%10);
			switchDigit(positions.eq(third),value%10);
		}
		
		return this;
	};


	function init(elem, options){
		elem.addClass('countdownHolder');

		// Creating the markup inside the container
		$.each(['Days','Hours','Minutes','Seconds'],function(i){
			var boxName;
			if(this=="Days") {
				boxName = "d";
			}
			else if(this=="Hours") {
				boxName = "h";
			}
			else if(this=="Minutes") {
				boxName = "m";
			}
			else {
				boxName = "s";
			}
			left = Math.floor((options.timestamp - (new Date())) / 1000);
			
			if(left < 0){
				left = 0;
			}
			
			// Number of days left
			d = Math.floor(left / days);
			var html = '<div class="count'+this+'">';
			if( this=="Days" && d >= 100 ) {
				html +=	'<span class="position">' +
					'<span class="digit static">0</span>' +
				'</span>';
			}
			html +=	'<span class="position">' +
					'<span class="digit static">0</span>' +
				'</span>' +
				'<span class="position">' +
					'<span class="digit static">0</span>' +
				'</span>' +
				'<span class="boxName">' +
					'<span class="'+this+'">' + boxName + '</span>' +
				'</span>'
			$( html ).appendTo(elem);
			
			// if(this!="Seconds"){
			// 	elem.append('<span class="points">:</span><span class="countDiv countDiv'+i+'"></span>');
			// }
		});

	}

	// Creates an animated transition between the two numbers
	function switchDigit(position,number){
		
		var digit = position.find('.digit')
		
		if(digit.is(':animated')){
			return false;
		}
		
		if(position.data('digit') == number){
			// We are already showing this number
			return false;
		}
		
		position.data('digit', number);
		
		var replacement = $('<span>',{
			'class':'digit',
			css:{
				top:0,
				opacity:0
			},
			html:number
		});
		
		// The .static class is added when the animation
		// completes. This makes it run smoother.
		
		digit
			.before(replacement)
			.removeClass('static')
			.animate({top:0,opacity:0},'fast',function(){
				digit.remove();
			})

		replacement
			.delay(100)
			.animate({top:0,opacity:1},'fast',function(){
				replacement.addClass('static');
			});
	}
})(jQuery);
