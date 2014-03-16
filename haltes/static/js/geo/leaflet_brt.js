// Definitions for BRT background map from https://github.com/bartvde/PDOK-Leaflet
// Resoluties (pixels per meter) van de zoomniveaus:
var res = [3440.640, 1720.320, 860.160, 430.080, 215.040, 107.520, 53.760, 26.880, 13.440, 6.720, 3.360, 1.680, 0.840, 0.420];

// Juiste projectieparameters voor Rijksdriehoekstelsel (EPSG:28992):
var RD = L.CRS.proj4js('EPSG:28992', '+proj=sterea +lat_0=52.15616055555555 +lon_0=5.38763888888889 +k=0.9999079 +x_0=155000 +y_0=463000 +ellps=bessel +units=m +towgs84=565.2369,50.0087,465.658,-0.406857330322398,0.350732676542563,-1.8703473836068,4.0812 +no_defs', new L.Transformation(1, 285401.920, -1, 903401.920));
RD.scale = function(zoom) {
  return 1 / res[zoom];
};
var brt_layer = new L.TileLayer('http://geodata.nationaalgeoregister.nl/tms/1.0.0/brtachtergrondkaart/{z}/{x}/{y}.png', {
  tms: true,
  minZoom: 3,
  maxZoom: 13,
  attribution: 'Kaartgegevens: © <a href="http://www.kadaster.nl">Kadaster</a>, <a href="http://openstreetmap.org">OpenStreetMap</a><span class="printhide">-auteurs (<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>).</span>',
  continuousWorld: true
});
