function geo_kml() {
	var thisUri = window.location.href;
	thisUri = thisUri.slice(0, thisUri.length - window.location.hash.length);

	viewInUse = thisUri.match('@?@?kml-openlayers\/?$');
	if (viewInUse && viewInUse.length == 1) {
	      thisUri = thisUri.replace(viewInUse[0], "");
	}

	if (!thisUri.match('\/$')) {
	      thisUri += '/';
	}

	kml = new OpenLayers.Layer.GML("KML Layer", thisUri + "@@kml-document",
	{
	    format: OpenLayers.Format.KML, 
	    projection: map.displayProjection,
	    formatOptions: {
		extractStyles: true, 
		extractAttributes: true
	    }
	})

	map.addLayer(kml);
	var select = new OpenLayers.Control.SelectFeature(kml);
	    
	kml.events.on({
	    "featureselected": onFeatureSelect,
	    "featureunselected": onFeatureUnselect
	});

	map.addControl(select);
	select.activate();

	function onPopupClose(evt) {
	    select.unselectAll();
	}
	function onFeatureSelect(event) {
	    var feature = event.feature;
	    var selectedFeature = feature;
	    var popup = new OpenLayers.Popup.FramedCloud("chicken", 
		feature.geometry.getBounds().getCenterLonLat(),
		new OpenLayers.Size(200,200),
		"<h2>"+feature.attributes.name + "</h2>" + feature.attributes.description,
		null, true, onPopupClose
	    );
	    feature.popup = popup;
	    map.addPopup(popup);
	}
	function onFeatureUnselect(event) {
	    var feature = event.feature;
	    if(feature.popup) {
		map.removePopup(feature.popup);
		feature.popup.destroy();
		delete feature.popup;
	    }
	}
}

jq(window).load(function() {
    geo_kml();
}); 

