/*global window, jQuery, document, OpenLayers*/

(function ($) {
    "use strict";
    $(window).bind('mapload', function (evt, widget) {
        var map = widget.map,
            kmls = map.getLayersByClass('OpenLayers.Layer.Vector'),
            select = new OpenLayers.Control.SelectFeature(kmls);

        function onPopupClose(evt) {
            select.unselectAll();
        }

        function onFeatureSelect(feature, arg1, arg2) {
            var text;
            if (feature.style.balloonStyle) {
                text = feature.style.balloonStyle.replace((/\$\{(.*?)\}/g), function(str, match) { 
                    var ret = feature.attributes[match] || '';
                    return typeof(ret) === 'object' ? ret.value: ret || '';
                });
            } else {
                text = "<h2>" + feature.attributes.name + "</h2>" + feature.attributes.description;
            }
            var popup = new OpenLayers.Popup.FramedCloud(
                "chicken",
                feature.geometry.getBounds().getCenterLonLat(),
                new OpenLayers.Size(200, 200),
                text,
                null,
                true,
                onPopupClose
            );
            feature.popup = popup;
            map.addPopup(popup);
        }

        function onFeatureUnselect(feature, arg1, arg2) {
            if (feature.popup) {
                map.removePopup(feature.popup);
                feature.popup.destroy();
                delete feature.popup;
            }
        }

        select.onSelect = onFeatureSelect;
        select.onUnselect = onFeatureUnselect;

        map.addControl(select);
        select.activate();

    });
}(jQuery));
