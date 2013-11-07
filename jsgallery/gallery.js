gallery = {
	SLIDES_WIDTH : 110,//THIS MUST BE SET TO THE WIDTH OF A SLIDE PLUS ALL ADDITIONAL WIDTH (margin, padding, etc)
	SLIDES_WINDOW_WIDTH : 440,//same with this
	
	start:function(){
		this.changeMainImage(slides[0]);//sets main image to be first image
		
		this.bindArrows();
		$('.exit').click(this.hideOverlayImage);
		
		for (var i = 0; i < slides.length; i++){//adds slides to the slideshow underneath
			this.addSlideImage(slides[i]);
		}
		$('.slides div').first().addClass('target');//sets initial 'target' image of slideshow
		
		
	},
	bindArrows : function(){//adds the click functions to all arrows in application
		var pthis = this;
		$('.slideshow .arrow.right').click(function(){
			var target = $('.target');
			if (target.next().length){
				//sets new target
				var slides = $('.slides');
				var left = slides.position().left;
				var otherleft = target.removeClass('target').next().addClass('target').position().left
				//moves slideshow if need be
				if (-left + pthis.SLIDES_WINDOW_WIDTH < otherleft + pthis.SLIDES_WIDTH){
					slides.css({left: (pthis.SLIDES_WINDOW_WIDTH - (otherleft + pthis.SLIDES_WIDTH)) + "px"});
				}
				pthis.changeMainImage($('.target img').attr('src'));
			}
		});
		$('.slideshow .arrow.left').click(function(){
			var target = $('.target');
			if (target.prev().length){
				//sets new target
				var slides = $('.slides');
				var left = slides.position().left;
				var otherleft = target.removeClass('target').prev().addClass('target').position().left
				//moves slide if need be
				if (-left > otherleft){
					slides.css({left: -otherleft + "px"});
				}
				pthis.changeMainImage($('.target img').attr('src'));
			}
		});
		$('.largeWindow .arrow.right').click(function(){
			if ($('.overlayTarget').next().length){
				$('.overlayTarget').removeClass('overlayTarget').next().addClass('overlayTarget')
				pthis.changeOverlayImage($('.overlayTarget img').attr('src'));
			}
		});
		$('.largeWindow .arrow.left').click(function(){
			if ($('.overlayTarget').prev().length){
				$('.overlayTarget').removeClass('overlayTarget').prev().addClass('overlayTarget')
				pthis.changeOverlayImage($('.overlayTarget img').attr('src'));
			}
		});
	},
	changeMainImage : function(image){//changes the main image of the application
		//variables
		var pthis = this;
		var mainwindow = $('.main.window');
		var img = new Image();
		img.src = image;
		
		img.onload = function(){
			var DOMImage = $('<img>');
			$(DOMImage).attr('src',image);
			
			pthis.fitImageToWindow(img,DOMImage,mainwindow);
			//CSS animation triggers
			$('img',mainwindow).removeClass('mainImage').addClass('goingOut');
			setTimeout(function(){$('img.goingOut',mainwindow).remove()},1000);
			
			mainwindow.append(DOMImage);
			DOMImage.click(function(){
				pthis.showOverlayImage(image);
			});
			setTimeout(function(){DOMImage.addClass('mainImage');},0);//CSS requires this to be a setTimeout to activate the transition
		};
	},
	
	addSlideImage : function(image){//adds an image to the slideshow
		var pthis = this;
		var slides = $('.slides');
		var img = new Image();
		img.src = image;
		
		var window = $('<div><img></div>');
		$('.slides').append(window);
		
		$(window).click(function(){//makes a slide the target of the slideshow if it is clicked on
			$('.target').removeClass('target')
			$(window).addClass('target');
			pthis.changeMainImage(image);
		});
		
		img.onload = function(){
			var DOMImage = $('img',window);
			DOMImage.attr('src',image);
			pthis.fitImageToWindow(img,DOMImage,window);
		};
	},
	
	fitImageToWindow : function(imageObject,DOMImage,window){//does math to fit the image as best as possible within the window it should fit into
		(imageObject.height/window.height())>(imageObject.width/window.width()) ? DOMImage.attr('height',window.height()) : DOMImage.attr('width',window.width());
	},
	
	showOverlayImage : function(image){//shows the large overlay image
		$('.target').addClass('overlayTarget');
		$('.largeWindowWrapper').css({"z-index" : '1'}).addClass('showOverlay');
		this.changeOverlayImage(image);
	},
	
	changeOverlayImage : function(image){
		img = new Image();
		img.src = image;
		var largeWindow = $('.largeWindow');
		var pthis = this;
		
		img.onload = function(){
			var DOMImage = $('<img class = "overlayImage">');
			$(DOMImage).attr('src',image);
			
			if ($('img.overlayImage',largeWindow).length){
				$('img.overlayImage',largeWindow).removeClass('mainImage');//fades out current image
				
				setTimeout(function(){//waits one second for the old image to fade out. you MUST change to whatever value if you change the length of the effect in CSS
					$('img.overlayImage',largeWindow).remove();
					largeWindow.append(DOMImage);
					pthis.fitImageToWindow(img,DOMImage,largeWindow);
					setTimeout(function(){DOMImage.addClass('mainImage');},0);
				},500);
			}
			else{
				largeWindow.append(DOMImage);
				pthis.fitImageToWindow(img,DOMImage,largeWindow);
				setTimeout(function(){DOMImage.addClass('mainImage');},0);
			}
		}
	},
	hideOverlayImage : function(){
		$('.overlayTarget').removeClass('overlayTarget');
		$('.largeWindowWrapper').removeClass('showOverlay');
		setTimeout(function(){
			$('.largeWindowWrapper').css({'z-index' : '-1'});
			$('.largeWindow .mainImage').remove();
		},1000);
	}
	
}

$(function(){gallery.start();});
