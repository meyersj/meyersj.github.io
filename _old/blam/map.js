function initmap() {
  // set up the map
  map = new L.Map('map');

  // create the tile layer with correct attribution
  //var tileUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
  var tileUrl='http://a.tiles.mapbox.com/v3/meyersj.map-6u6rh54c/{z}/{x}/{y}.png';
  var attrib='Map data &copy; OpenStreetMap contributors, Designs &copy; Mapbox';
  var tiles = new L.TileLayer(tileUrl, {minZoom: 5, maxZoom: 20, attribution: attrib});	 	

  // Portland
  map.setView(new L.LatLng(45.512326, -122.6429570), 13);
  map.addLayer(tiles);
}



