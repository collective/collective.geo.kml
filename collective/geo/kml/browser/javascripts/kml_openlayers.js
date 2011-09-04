jq(window).bind('load', function() {
    var map = cgmap.config['default-cgmap'].map;

    var kmls = map.getLayersByClass('OpenLayers.Layer.GML');
    var select = new OpenLayers.Control.SelectFeature(kmls);
    select.onSelect = onFeatureSelect;
    select.onUnselect = onFeatureUnselect;

    map.addControl(select);
    select.activate();

    function onPopupClose(evt) {
        select.unselectAll();
    }

    function onFeatureSelect(feature, arg1, arg2) {
        var popup = new OpenLayers.Popup.FramedCloud(
            "chicken",
            feature.geometry.getBounds().getCenterLonLat(),
            new OpenLayers.Size(200,200),
            "<h2>"+feature.attributes.name + "</h2>" + feature.attributes.description,
            null, true, onPopupClose
        );
        feature.popup = popup;
        map.addPopup(popup);
    }

    function onFeatureUnselect(feature, arg1, arg2) {
        if(feature.popup) {
            map.removePopup(feature.popup);
            feature.popup.destroy();
            delete feature.popup;
        }
    }

});
