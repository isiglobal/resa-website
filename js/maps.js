/**
 * RESA map, adapted from 'Google Maps Tour Stops'
 * TODO: Backbone this stuff!
 * TODO: Organize and cleanup!
 * Copyright (c) 2013 Brandon Thomas <bt@brand.io>
 * See more at http://brand.io
 */

// Resize breakpoints -- may need to move to main.js
BREAKPOINTS = {
	PHONE_PORTRAIT: 479, // < 480
	PHONE_LANDSCAPE: 599, // 480 - 599
	TABLET_PORTRAIT: 768, // 600 - 768
	TABLET_LANDSCAPE: 1024, // 769 - 1024
	DESKTOP_REGULAR: 1280, // 1025 - 1280
	// DESKTOP_HUGE >= 1281
}

var GOOGLE_ICON_IMG = '/static/assets/img/icons/pin_18.png';

function initialize_maps() 
{
	var resa = new google.maps.LatLng(33.235924, -84.826988),
		mapOptions = {
			center: resa,
			zoom: 15,
			draggable: true,
			disableDefaultUI: false,
			panControl: true,
			zoomControl: true,
			mapTypeControl: true,
			scaleControl: true,
			streetViewControl: true,
			overviewMapControl: true,
			disableDoubleClickZoom: false,
			scrollwheel: true,
			mapTypeId: google.maps.MapTypeId.ROADMAP,
		},
		center = resa;

	// New post-Google IO design
	google.maps.visualRefresh = true;

	var mark = new google.maps.Marker({
		position: resa,
		draggable: false,
		clickable: true,
		flat: true,
		map: map,
		title: 'West GA Resa',
		zIndex: 90000,
		visible: true,
		//icon: GOOGLE_ICON_IMG,
		//shadow: SHADOW_IMG,
	});

	// I believe removing the 'report error' link falls within
	// Google's usage terms. If they tell us no, we can revert
	// back. <http://stackoverflow.com/a/11625444>
	var styleOptions = {
		name: 'No Report Error',
	};

	var MAP_STYLE = [{
		featureType: 'road',
		elementType: 'all',
		stylers: [
			{ visibility: 'on' }
		]
	}];

	var map = new google.maps.Map(
		document.getElementById('maps'),
		mapOptions);

	mark.setMap(map);

	var mapType = new google.maps.StyledMapType(MAP_STYLE, 
		styleOptions);

	map.mapTypes.set('No Report Error', mapType);
	map.setMapTypeId('No Report Error');

	/**
	 * Resize events code
	 */
	var sizeMap = function() {
		var width = $('#maps').width();
		if(width <= BREAKPOINTS.PHONE_PORTRAIT) {
			map.setZoom(15);
			map.setCenter(resa);
			center = resa;
		}
		else if(width <= BREAKPOINTS.PHONE_LANDSCAPE) {
			map.setZoom(15);
			map.setCenter(resa);
			center = resa;
		}
		else if(width <= BREAKPOINTS.TABLET_PORTRAIT) {
			map.setZoom(15);
			map.setCenter(resa);
			center = resa;
		}
		else if(width <= BREAKPOINTS.TABLET_LANDSCAPE) {
			map.setZoom(15);
			map.setCenter(resa);
			center = resa;
		}
		else if(width <= BREAKPOINTS.DESKTOP_REGULAR) {
			map.setZoom(14);
			map.setCenter(resa);
			center = resa;
		}
		else { // We're at width >= DESKTOP_HUGE
			map.setZoom(14);
			map.setCenter(resa);
			center = resa;
		}
	}
	$(window).on('resize', sizeMap);

	google.maps.event.addListener(map, 'dragend', function() {
		setTimeout(function() {
			map.panTo(center);
		}, 400);
	});
}
