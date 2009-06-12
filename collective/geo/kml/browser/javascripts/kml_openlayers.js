kml = new OpenLayers.Layer.GML("Boulders", "@@kml-document", 
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