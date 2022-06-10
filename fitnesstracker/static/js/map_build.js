// Create the map
var map = L.map('map').setView([53.299697,-4.387321], 10);

osm = L.tileLayer('https://api.maptiler.com/maps/basic/{z}/{x}/{y}.png?key=LHlqrAvd3VUM4yZjqFDy', {
attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
});
osm.addTo(map);

// Add the route to the map
fetch('https://api.maptiler.com/data/b92719af-8d5b-4006-9631-3d8b13eaa1c6/features.json?key=g9ErshPDnj0LYYtEd10o')
	.then(function (responce) {
	return responce.json();
	})
	.then(function (data) {
      L.geoJSON(data).addTo(map);
	});

// Add the start / lap checkered flag
  var checkerd = L.icon ({
    iconUrl: "static/images/markers/checkered-flag.png",
    iconSize: [60, 60],
    iconAnchor: [5, 60]
  });

  var start = L.marker([53.2648, -4.0897],{icon:checkerd}).addTo(map);

  // Add unique markers for each group member
  var mapMarkers = [
    L.icon({
        iconUrl: 'static/images/markers/runner-yellow.png',
      iconSize: [30, 30],
          iconAnchor: [15, 15],
         popupAnchor: [5, 5]
    }),
    L.icon({
        iconUrl: 'static/images/markers/runner-green.png',
      iconSize: [30, 30],
          iconAnchor: [15, 15],
         popupAnchor: [5, 5]
    }),
   L.icon({
        iconUrl: 'static/images/markers/runner-red.png',
      iconSize: [30, 30],
          iconAnchor: [15, 15],
         popupAnchor: [5, 5]
    }),
    L.icon({
        iconUrl: 'static/images/markers/runner-pink.png',
      iconSize: [30, 30],
          iconAnchor: [15, 15],
         popupAnchor: [5, 5]
    }),
    L.icon({
        iconUrl: 'static/images/markers/runner-blue.png',
      iconSize: [30, 30],
          iconAnchor: [15, 15],
         popupAnchor: [5, 5]
    }),
  L.icon({
        iconUrl: 'static/images/markers/runner-orange.png',
      iconSize: [30, 30],
          iconAnchor: [15, 15],
         popupAnchor: [5, 5]
    }),
    L.icon({
        iconUrl: 'static/images/markers/runner-d-blue.png',
      iconSize: [30, 30],
          iconAnchor: [15, 15],
         popupAnchor: [5, 5]
    }),
   L.icon({
        iconUrl: 'static/images/markers/runner-lime.png',
      iconSize: [30, 30],
          iconAnchor: [15, 15],
         popupAnchor: [5, 5]
    }),
    L.icon({
        iconUrl: 'static/images/markers/runner-l-blue.png',
      iconSize: [30, 30],
          iconAnchor: [15, 15],
         popupAnchor: [5, 5]
    }),
    L.icon({
        iconUrl: 'static/images/markers/runner-purple.png',
      iconSize: [30, 30],
          iconAnchor: [15, 15],
         popupAnchor: [5, 5]
    }),
  L.icon({
        iconUrl: 'static/images/markers/runner-navy.png',
      iconSize: [30, 30],
          iconAnchor: [15, 15],
         popupAnchor: [5, 5]
    }),
    L.icon({
        iconUrl: 'static/images/markers/runner-rose.png',
      iconSize: [30, 30],
          iconAnchor: [15, 15],
         popupAnchor: [5, 5]
    }),
    L.icon({
        iconUrl: 'static/images/markers/runner-slate.png',
      iconSize: [30, 30],
          iconAnchor: [15, 15],
         popupAnchor: [5, 5]
    }),
  L.icon({
        iconUrl: 'static/images/markers/runner-brown.png',
      iconSize: [30, 30],
          iconAnchor: [15, 15],
         popupAnchor: [5, 5]
    }),
    L.icon({
        iconUrl: 'static/images/markers/runner-white.png',
      iconSize: [30, 30],
          iconAnchor: [15, 15],
         popupAnchor: [5, 5]
    })
];
