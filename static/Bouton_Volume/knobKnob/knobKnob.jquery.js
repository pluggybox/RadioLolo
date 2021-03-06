/**
 * @name		jQuery KnobKnob plugin
 * @author		Martin Angelov
 * @version 	1.0
 * @url			http://tutorialzine.com/2011/11/pretty-switches-css3-jquery/
 * @license		MIT License
 */
$(function(){

	$('#control').knobKnob({
		value: VALEUR_DEPART_BOUTON,
	});

});


var ANGLE_MIN = 10.0;
var ANGLE_MAX = 350.0;

(function($){
	
	$.fn.knobKnob = function(props){
	
		var options = $.extend({
			value: 0
		}, props || {});
	
		var tpl = '<div class="knob">\
				<div class="top"></div>\
				<div class="base"></div>\
			</div>';
	
		return this.each(function(){
			
			var el = $(this);
			el.append(tpl);
			
			var knob = $('.knob',el),
				knobTop = knob.find('.top'),
				startDeg = -1,
				currentDeg = ANGLE_MIN,
				rotation = ANGLE_MIN,
				doc = $(document);
			
			if(options.value > 0 && options.value <= 359){
				rotation = currentDeg = options.value;
				knobTop.css('transform','rotate('+(currentDeg)+'deg)');
			}
			
			knob.on('mousedown touchstart', function(e){
				e.preventDefault();
			
				var offset = knob.offset();
				var center = {
					y : offset.top + knob.height()/2,
					x: offset.left + knob.width()/2
				};
				
				var a, b, deg, tmp,
					rad2deg = 180/Math.PI;
				
				knob.on('mousemove.rem touchmove.rem',function(e){
					
					e = (e.originalEvent.touches) ? e.originalEvent.touches[0] : e;
					
					a = center.y - e.pageY;
					b = center.x - e.pageX;
					deg = Math.atan2(a,b)*rad2deg;

					// we have to make sure that negative
					// angles are turned into positive:
					if(deg<0){
						deg = 360 + deg;
					}
					
					// Save the starting position of the drag
					if(startDeg == -1){
						startDeg = deg;
					}
					
					// Calculating the current rotation
					tmp = Math.floor((deg-startDeg) + rotation);
                    if(tmp < ANGLE_MIN)
                    {
                    	tmp = ANGLE_MIN;
                    }
                    if(tmp > ANGLE_MAX)
                    {
                    	tmp = ANGLE_MAX;
                    }

					// This would suggest we are at an end position;
					// we need to block further rotation.
					if(Math.abs(tmp - currentDeg) > 180){
						return false;
					}

					currentDeg = tmp;
					knobTop.css('transform','rotate('+(currentDeg)+'deg)');

					document.getElementById("volume").innerHTML = Math.round((100*(currentDeg - ANGLE_MIN))/(ANGLE_MAX - ANGLE_MIN)) +'%';
				});
			
				doc.on('mouseup.rem  touchend.rem',function(){
					knob.off('.rem');
					doc.off('.rem');
					
					// Saving the current rotation
					rotation = currentDeg - ANGLE_MIN;
					
					// Marking the starting degree as invalid
					startDeg = -1;

					//document.getElementById("myForm").submit();
					document.getElementById("changer_volume").value = Math.round((100*(currentDeg - ANGLE_MIN))/(ANGLE_MAX - ANGLE_MIN));
					document.getElementById("changer_volume").click()
				});
			
			});
		});
	};
	
})(jQuery);
