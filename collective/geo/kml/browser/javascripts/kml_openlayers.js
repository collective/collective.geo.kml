// funzia
//         var lon = 5;
//         var lat = 40;
//         var zoom = 5;
//         var map, layer;
// 
//         function openlayers_init(){
//             map = new OpenLayers.Map('map');
//             layer = new OpenLayers.Layer.WMS( "OpenLayers WMS",
//                     "http://labs.metacarta.com/wms/vmap0", {layers: 'basic'} );
//             map.addLayer(layer);
//             map.addLayer(new OpenLayers.Layer.GML("KML", "@@kml-document", 
//                {
//                 format: OpenLayers.Format.KML, 
//                 formatOptions: {
//                   extractStyles: true, 
//                   extractAttributes: true,
//                   maxDepth: 2
//                 }
//                }));
//             map.zoomToExtent(new OpenLayers.Bounds(-112.306698,36.017792,-112.03204,36.18087));
//         }



// ok funzia
//         var lon = 5;
//         var lat = 40;
//         var zoom = 5;
//         var map, layer;
// 
//         function openlayers_init(){
//             map = new OpenLayers.Map('map');
//             layer = new OpenLayers.Layer.WMS( "OpenLayers WMS",
//                     "http://labs.metacarta.com/wms/vmap0", {layers: 'basic'} );
//             map.addLayer(layer);
//             map.addLayer(new OpenLayers.Layer.GML("KML", "@@kml-document", 
//                {
//                 format: OpenLayers.Format.KML, 
//                 formatOptions: {
//                   extractStyles: true, 
//                   extractAttributes: true
//                 }
//                }));
//              selectControl = new OpenLayers.Control.SelectFeature(map.layers[1],
//                 {onSelect: onFeatureSelect, onUnselect: onFeatureUnselect});
//   
//             mousecontrol = new OpenLayers.Control.MousePosition(),
//             map.addControl(mousecontrol);
// 
//             map.addControl(selectControl);
//             selectControl.activate();   
//             map.zoomToExtent(new OpenLayers.Bounds(68.774414,11.381836,123.662109,34.628906));
//         }
//         function onPopupClose(evt) {
//             selectControl.unselect(selectedFeature);
//         }
//         function onFeatureSelect(feature) {
//             selectedFeature = feature;
//             // Since KML is user-generated, do naive protection against
//             // Javascript.
//             var content = "<h2>"+feature.attributes.name + "</h2>" + feature.attributes.description;
//             if (content.search("<script") != -1) {
//                 content = "Content contained Javascript! Escaped content below.<br />" + content.replace(/</g, "&lt;");
//             }
//             popup = new OpenLayers.Popup.FramedCloud("chicken", 
//                                      feature.geometry.getBounds().getCenterLonLat(),
//                                      new OpenLayers.Size(100,100),
//                                      content,
//                                      null, true, onPopupClose);
//             feature.popup = popup;
//             map.addPopup(popup);
//         }
//         function onFeatureUnselect(feature) {
//             map.removePopup(feature.popup);
//             feature.popup.destroy();
//             feature.popup = null;
//         }

// var lon = 5;
// var lat = 40;
// var zoom = 5;
var map, select, satellite, kml, ibrida;

function openlayers_init(){
    var options = {
        projection: new OpenLayers.Projection("EPSG:900913"),
        displayProjection: new OpenLayers.Projection("EPSG:4326"),
        units: "m",
        maxResolution: 156543.0339,
        maxExtent: new OpenLayers.Bounds(-20037508.34, -20037508.34,
                                         20037508.34, 20037508.34)
    };

    map = new OpenLayers.Map('map', options);

    if (!googlemaps) {
        var mapnik = new OpenLayers.Layer.TMS(
            "Mappa stradale (OpenStreetMap)",
            "http://tile.openstreetmap.org/",
            {
                type: 'png', getURL: osm_getTileURL,
                displayOutsideMaxExtent: true,
                attribution: '<a href="http://www.openstreetmap.org/">OpenStreetMap</a>'
            }
        );

        map.addLayer(mapnik);
    }


   if (googlemaps) {
    // create Google Mercator layers
        var gmap = new OpenLayers.Layer.Google(
            "Google",
            {'sphericalMercator': true}
        );

        map.addLayer(gmap);

        satellite = new OpenLayers.Layer.Google(
            "Satellite (Google)" , {type: G_SATELLITE_MAP, 'sphericalMercator': true}
        );

        map.addLayer(satellite);

        ibrida = new OpenLayers.Layer.Google(
            "Ibrida (Google)" , {type: G_HYBRID_MAP, 'sphericalMercator': true}
        );

        map.addLayer(ibrida);    
    }


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

    select = new OpenLayers.Control.SelectFeature(kml);
    
    kml.events.on({
        "featureselected": onFeatureSelect,
        "featureunselected": onFeatureUnselect
    });

    map.addControl(select);
    select.activate();   

    map.addControl(new OpenLayers.Control.LayerSwitcher());

    mousecontrol = new OpenLayers.Control.MousePosition(),
    map.addControl(mousecontrol);


    map.setCenter(new OpenLayers.LonLat(lon,lat).transform(map.displayProjection, map.projection), zoom);

//     map.zoomToExtent(new OpenLayers.Bounds(8.09006,45.76058,8.45604,45.64597).transform(map.displayProjection, map.projection));
}
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
function osm_getTileURL(bounds) {
    var res = this.map.getResolution();
    var x = Math.round((bounds.left - this.maxExtent.left) / (res * this.tileSize.w));
    var y = Math.round((this.maxExtent.top - bounds.top) / (res * this.tileSize.h));
    var z = this.map.getZoom();
    var limit = Math.pow(2, z);

    if (y < 0 || y >= limit) {
        return OpenLayers.Util.getImagesLocation() + "404.png";
    } else {
        x = ((x % limit) + limit) % limit;
        return this.url + z + "/" + x + "/" + y + "." + this.type;
    }
}
