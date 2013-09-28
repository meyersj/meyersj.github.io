function initmap() {
  // set up the map
  map = new L.Map('map');

  // create the tile layer with correct attribution
  var tileUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
  //var tileUrl='http://a.tiles.mapbox.com/v3/meyersj.map-6u6rh54c/{z}/{x}/{y}.png';
  var attrib='Map data &copy; OpenStreetMap contributors, Designs &copy; Mapbox';
  var tiles = new L.TileLayer(tileUrl, {minZoom: 8, maxZoom: 20, attribution: attrib});	 	

  // Portland
  map.setView(new L.LatLng(45.524, -122.675),12);
  map.addLayer(tiles);
}


L.NumberedDivIcon = L.Icon.extend({
  options: {
  // EDIT THIS TO POINT TO THE FILE AT http://www.charliecroom.com/marker_hole.png (or your own marker)
    //iconUrl: 'https://dl.dropbox.com/s/jyg63oqrs83xtl6/marker_hole.png',
    iconUrl: 'http://dl.dropbox.com/s/vh7fr9sc9pobesk/marker_hole2.png',

    number: '',
    shadowUrl: null,
    iconSize: new L.Point(25, 41),
    iconAnchor: new L.Point(13, 41),
    popupAnchor: new L.Point(0, -33),
    /*
    iconAnchor: (Point)
    popupAnchor: (Point)
    */
    className: 'leaflet-div-icon'
  },
 
  createIcon: function () {
    var div = document.createElement('div');
    var img = this._createImg(this.options['iconUrl']);
    var numdiv = document.createElement('div');
    numdiv.setAttribute ( "class", "number" );
    numdiv.innerHTML = this.options['number'] || '';
    div.appendChild ( img );
    div.appendChild ( numdiv );
    this._setIconStyles(div, 'icon');
    return div;
  },
 
  //you could change this to add a shadow like in the normal marker if you really wanted
  createShadow: function () {
    return null;
  }
});

